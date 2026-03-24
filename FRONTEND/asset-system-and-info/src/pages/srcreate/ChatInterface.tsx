'use client';

import { useState, useOptimistic, useRef, useEffect, useActionState, startTransition } from 'react';
import { Bot, User, Send, Loader2, Mic } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { cn } from '@/lib/utils';
import { Card } from '@/components/ui/card';
import { handleSrCreateChat } from './handleSrCreateChat';
import { useToast } from '@/hooks/use-toast';

type Message = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  isOptimistic?: boolean;
};

type ChatState = {
  thread_id? :string |null;
    aiMessage: {
      content: string;
    } | null;
    error: {
      request?: string[];
    } | null;
    issrcreated : boolean |null ;
  };

const initialState: ChatState = {
  aiMessage: null,
  error: null,
  thread_id :null,
  issrcreated : null
};

export function ChatInterface() {
  const [state, formAction, isPending] = useActionState<ChatState, FormData>(handleSrCreateChat, initialState);
  const [messages, setMessages] = useState<Message[]>([]);
  const formRef = useRef<HTMLFormElement>(null);
  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();
  const [optimisticMessages, addOptimisticMessage] = useOptimistic<Message[], string>(
    messages,
    (currentMessages, newMessageContent) => [
      ...currentMessages,
      {
        id: crypto.randomUUID(),
        role: 'user',
        content: newMessageContent,
        isOptimistic: true,
      },
    ]
  );

  
  const [isListening, setIsListening] = useState(false);

// Inside your ChatInterface component
const recognitionRef = useRef<any>(null);


const toggleListening = () => {
  if (isListening) {
    recognitionRef.current?.stop();
    return;
  }

  const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
  if (!SpeechRecognition) {
    alert('Speech recognition not supported in this browser.');
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.lang = 'en-US';
  recognition.interimResults = true;
  recognition.continuous = true;

  // Track the text that was already in the input before we started
  let baseText = "";

  recognition.onstart = () => {
    setIsListening(true);
    const input = formRef.current?.querySelector<HTMLInputElement>('input[name="request"]');
    if (input) {
      // If there's already text, add a space so the new words don't stick to it
      baseText = input.value + (input.value ? ' ' : '');
    }
  };

  recognition.onresult = (event: any) => {
    const input = formRef.current?.querySelector<HTMLInputElement>('input[name="request"]');
    if (!input) return;

    let interimTranscript = '';
    let finalTranscript = '';

    for (let i = event.resultIndex; i < event.results.length; i++) {
      const transcript = event.results[i][0].transcript;
      if (event.results[i].isFinal) {
        finalTranscript += transcript;
      } else {
        interimTranscript += transcript;
      }
    }

    // Update the input: Original Text + what was just finalized + what is currently being said
    input.value = baseText + finalTranscript + interimTranscript;
    
    // Update baseText if we got a final result so it stays persistent
    if (finalTranscript) {
       baseText += finalTranscript;
    }
  };

  recognition.onerror = () => setIsListening(false);
  recognition.onend = () => setIsListening(false);

  recognitionRef.current = recognition;
  recognition.start();
};
useEffect(() => {
    if (state?.aiMessage) {
      setMessages((prev) => [
        ...prev,
        {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: state.aiMessage!.content,
        },
      ]);
    }
  }, [state]); // Runs whenever the action state changes
  useEffect(() => {
    if (state?.issrcreated) {
      toast({
        title: "Request Confirmed",
        description: "Your service request is now in the system.",
        variant: "default", // or "destructive" if state.error exists
      });
    }

    if (state?.error) {
      toast({
        variant: "destructive", // This triggers the red error styling
        title: "Uh oh! Something went wrong.",
        description: "There was a problem with your request.",
      });
    }
  }, [state?.issrcreated,state?.error, toast]);
const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const message = formData.get('request') as string;
  
    if (!message.trim() || isPending) return;
  
    // 1. Clear the input immediately
    formRef.current?.reset();
  
    // 2. Wrap in startTransition for useOptimistic to work
    startTransition(() => {
      addOptimisticMessage(message);
      
      // 3. Add the user message to permanent state so it stays 
      // after the optimistic state clears
      setMessages((prev) => [
        ...prev, 
        { id: crypto.randomUUID(), role: 'user', content: message }
      ]);
  
      // 4. Fire the action
      formAction(formData);
    });
  };



  return (
    <Card className="flex flex-col h-[calc(100vh-8rem)]">
      <div ref={scrollAreaRef} className="flex-1 overflow-y-auto p-6 space-y-6">
        {optimisticMessages.length === 0 ? (
          <div className="flex h-full items-center justify-center">
            <div className="text-center p-8 bg-muted/50 rounded-lg">
              <Bot className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-lg font-semibold text-foreground">Service Request  Assistant</h3>
              <p className="text-muted-foreground">Describe Issue Ai will analyze and create SR!</p>
            </div>
          </div>
        ) : (
          optimisticMessages.map((message) => (
            <div
              key={message.id}
              className={cn(
                'flex items-start gap-4',
                message.role === 'user' ? 'justify-end' : 'justify-start',
                message.isOptimistic ? 'opacity-50' : ''
              )}
            >
              {message.role === 'assistant' && (
                <Avatar className="w-8 h-8 border-2 border-primary">
                  <AvatarFallback className="bg-primary text-primary-foreground">
                    <Bot size={18} />
                  </AvatarFallback>
                </Avatar>
              )}
              <div
                className={cn(
                  'max-w-md rounded-lg px-4 py-3',
                  message.role === 'user'
                    ? 'bg-primary text-primary-foreground rounded-br-none'
                    : 'bg-muted text-muted-foreground rounded-bl-none'
                )}
              >
               
                  <p className="text-sm whitespace-pre-wrap">{message.content}</p>
              </div>
              {message.role === 'user' && (
                <Avatar className="w-8 h-8 border-2 border-muted">
                  <AvatarFallback>
                    <User size={18} />
                  </AvatarFallback>
                </Avatar>
              )}
            </div>
          ))
        )}
        {isPending && (
          <div className="flex items-start gap-4 justify-start">
            <Avatar className="w-8 h-8 border-2 border-primary">
              <AvatarFallback className="bg-primary text-primary-foreground">
                <Bot size={18} />
              </AvatarFallback>
            </Avatar>
            <div className="max-w-md rounded-lg px-4 py-3 bg-muted text-muted-foreground rounded-bl-none flex items-center">
              <Loader2 className="h-5 w-5 animate-spin text-primary" />
            </div>
          </div>
        )}
      </div>
      <div className="border-t p-4 bg-background">
        <form ref={formRef} onSubmit={handleSubmit} className="flex items-center gap-2">
        <input type="hidden" name="thread_id" value={state?.thread_id || ''} />
          <Input
            name="request"
            placeholder="Ask the AI something..."
            autoComplete="off"
            disabled={isPending}
            className="flex-1"
          />
        <Button 
  type="button" 
  size="icon" 
  onClick={toggleListening} 
  disabled={isPending}
  className={cn(
    "transition-all",
    isListening ? "bg-red-500 hover:bg-red-600 animate-pulse ring-2 ring-red-200" : ""
  )}
>
  {isListening ? (
    <Mic className="h-4 w-4 text-white" />
  ) : (
    <Mic className="h-4 w-4" />
  )}
</Button>
          <Button type="submit" size="icon" disabled={isPending}>
            <Send className="h-4 w-4" />
          </Button>
        </form>
        {/* {state?.error && (
          <p className="text-sm text-destructive mt-2">{state.error.request}</p>
        )} */}
      </div>
    </Card>
  );
}