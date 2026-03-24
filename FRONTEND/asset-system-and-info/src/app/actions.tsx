'use server';

import { determineContentType } from '@/ai/flows/display-ai-responses';
import { z } from 'zod';

const aiResponses = [
  "That's a great question! Based on the project goals, I'd recommend focusing on a recurrent neural network (RNN) architecture, specifically an LSTM, to handle the sequential nature of your data.",
  "I can help with that. Here's a simple boilerplate in HTML for you to get started: \n<div style='border: 1px solid hsl(var(--border)); padding: 1rem; border-radius: 0.5rem; background-color: hsl(var(--card));'>\n  <h3 style='font-weight: 600; margin-bottom: 0.5rem;'>Project Starter</h3>\n  <p>This is a basic HTML structure to demonstrate rendering.</p>\n</div>",
  "Could you elaborate on the dataset you are using? The choice of model is highly dependent on the data's characteristics. For example, is it structured or unstructured?",
  "To visualize your results, you could use a library like D3.js or Chart.js. Here is a list of potential chart types to consider: <ul style='list-style-type: disc; padding-left: 20px; margin-top: 0.5rem;'><li>Bar Chart for feature comparison</li><li>Line Chart for time-series data</li><li>Scatter Plot to see correlations</li></ul>",
  "An interesting approach would be to use transfer learning. By starting with a model pre-trained on a large dataset like ImageNet, you can significantly reduce training time and improve performance, even with a smaller dataset.",
];

const chatSchema = z.object({
  message: z.string().min(1, "Message cannot be empty."),
  projectId: z.string(),
});

type ChatState = {
  aiMessage: {
    content: string;
    type: 'html' | 'text';
  } | null;
  error: {
    message?: string[];
  } | null;
}

export async function handleChatMessage(prevState: ChatState, formData: FormData): Promise<ChatState> {
  const validatedFields = chatSchema.safeParse({
    message: formData.get('message'),
    projectId: formData.get('projectId'),
  });

  if (!validatedFields.success) {
    return {
      aiMessage: null,
      error: validatedFields.error.flatten().fieldErrors,
    };
  }
  
  // Simulate AI processing delay
  await new Promise(resolve => setTimeout(resolve, 1500));
  
  const aiResponse = aiResponses[Math.floor(Math.random() * aiResponses.length)];
  
  const { contentType } = await determineContentType(aiResponse);

  return {
    aiMessage: {
      content: aiResponse,
      type: contentType
    },
    error: null,
  };
}
