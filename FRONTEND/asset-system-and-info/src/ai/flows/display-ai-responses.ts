// src/ai/flows/display-ai-responses.ts
/**
 * @fileOverview Determines whether an AI response is HTML or plain text.
 */

export type DetermineContentTypeInput = string;
export type DetermineContentTypeOutput = {
  contentType: 'html' | 'text';
};

/**
 * Simple client-side function to check if a string contains HTML tags.
 */
export function determineContentType(
  input: DetermineContentTypeInput
): DetermineContentTypeOutput {
  // Regex to detect HTML tags
  const htmlTagRegex = /<\/?[a-z][\s\S]*>/i;
  const hasHTML = htmlTagRegex.test(input);

  return {
    contentType: hasHTML ? 'html' : 'text',
  };
}