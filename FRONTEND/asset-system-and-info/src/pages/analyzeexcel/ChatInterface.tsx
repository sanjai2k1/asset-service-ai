'use client';

import { useState, useOptimistic, useRef, useEffect, startTransition } from 'react';
import { Bot, User, Send, Loader2, Mic, Paperclip } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import { cn } from '@/lib/utils';
import { Card } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';
import { v4 as uuidv4 } from "uuid";
import { streamRequest } from '@/lib/api-client';

type Message = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  isOptimistic?: boolean;
};

type ChatState = {
  thread_id?: string | null;
  aiMessage: {
    content: string;
  } | null;
  error: {
    request?: string[];
  } | null;
  issrcreated: boolean | null;
};

const initialState: ChatState = {
  aiMessage: null,
  error: null,
  thread_id: null,
  issrcreated: null
};

interface AskResponse {
  thread_id?: string | null;
  aiMessage: {
    content: string;
  };
  issrcreated: boolean | null;
}

export function ChatInterface() {
  const [state, setState] = useState<ChatState>(initialState);
  const [isPending, setIsPending] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]); // ✅ FIXED
  const [agentStatus, setAgentStatus] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null);

  const formRef = useRef<HTMLFormElement>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const scrollAreaRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();

  const [optimisticMessages, addOptimisticMessage] = useOptimistic<Message[], string>(
    messages,
    (currentMessages, newMessageContent) => [
      ...currentMessages,
      {
        id: uuidv4(),
        role: 'user',
        content: newMessageContent,
        isOptimistic: true,
      },
    ]
  );

  const [isListening, setIsListening] = useState(false);
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

    let baseText = "";

    recognition.onstart = () => {
      setIsListening(true);
      const input = formRef.current?.querySelector<HTMLInputElement>('input[name="request"]');
      if (input) {
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

      input.value = baseText + finalTranscript + interimTranscript;

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
    const el = scrollAreaRef.current;
    if (!el) return;
  
    el.scrollTo({
      top: el.scrollHeight,
      behavior: "smooth",
    });
  }, [optimisticMessages]);

  // ✅ keep toast logic
  useEffect(() => {
    if (state?.issrcreated) {
      toast({
        title: "Request Confirmed",
        description: "Your service request is now in the system.",
      });
    }

    if (state?.error) {
      toast({
        variant: "destructive",
        title: "Uh oh! Something went wrong.",
        description: "There was a problem with your request.",
      });
    }
  }, [state?.issrcreated, state?.error, toast]);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const message = formData.get('request') as string;
  
    if (!message.trim() || isPending) return;
  
    formRef.current?.reset();
  
    // optimistic UI
    startTransition(() => {
      addOptimisticMessage(message);
  
      setMessages((prev) => [
        ...prev,
        { id: uuidv4(), role: 'user', content: message }
      ]);
    });
  
    setIsPending(true);
    setAgentStatus("Starting..."); // optional initial state
  
    try {
      await streamRequest<AskResponse>({
        url: "srcreation/ask-stream",
        data: { request: message, thread_id: state?.thread_id },
  
        onMessage: (data) => {
          if (data.type === "progress") {
            // 🔥 force immediate UI update
            setAgentStatus(data.current_node);
          }
  
          if (data.type === "final") {
            // 🔥 stop loader ONLY here
            setAgentStatus(null);
            setIsPending(false);
  
            setMessages((prev) => [
              ...prev,
              {
                id: uuidv4(),
                role: 'assistant',
                content: data.aiMessage.content,
              },
            ]);
  
            setState((prev: any) => ({
              ...prev,
              thread_id: data.issrcreated ? null : data.thread_id,
              issrcreated: data.issrcreated,
              error: null
            }));
          }
        },
  
        onError: () => {
          setAgentStatus("Error...");
          setIsPending(false);
        }
      });
    } catch (err) {
      setAgentStatus("Error...");
      setIsPending(false);
    }
  };

  return (
    <Card className="flex flex-col h-[calc(100vh-8rem)]">
      <div ref={scrollAreaRef} className="flex-1 overflow-y-auto p-6 space-y-6">
        {optimisticMessages.length === 0 ? (
          <div className="flex h-full items-center justify-center">
            <div className="text-center p-8 bg-muted/50 rounded-lg">
              <Bot className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-lg font-semibold text-foreground">Excel Analyzer</h3>
              <p className="text-muted-foreground">Start analysis by chat !</p>
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

        {(isPending || agentStatus) && (
          <div className="flex items-start gap-4 justify-start">
            <Avatar className="w-8 h-8 border-2 border-primary">
              <AvatarFallback className="bg-primary text-primary-foreground">
                <Bot size={18} />
              </AvatarFallback>
            </Avatar>

            <div className="max-w-md rounded-lg px-4 py-3 bg-muted text-muted-foreground rounded-bl-none flex items-center gap-2">
              <Loader2 className="h-5 w-5 animate-spin text-primary" />
              <span className="text-sm">
                {agentStatus || "Thinking..."}
              </span>
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
 {/* Hidden File Input */}
 <input
      type="file"
      name="excel"
      ref={fileInputRef}
      accept=".xls,.xlsx"
      className="hidden"
      onChange={(e) => {
        const selectedFile = e.target.files?.[0] || null;
        setFile(selectedFile);
      }}
    />

    {/* Attachment Button */}
    <Button
  type="button"
  size="icon"
  onClick={() => fileInputRef.current?.click()}
  disabled={isPending}
  className={cn(
    "transition-all text-primary-foreground",
    file
      ? "bg-green-500 hover:bg-green-600"
      : "bg-primary hover:bg-primary/90"
  )}
>
  <Paperclip className="h-4 w-4" />
</Button>
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
            <Mic className="h-4 w-4" />
          </Button>

          <Button type="submit" size="icon" disabled={isPending}>
            <Send className="h-4 w-4" />
          </Button>
        </form>
      </div>
    </Card>
  );
}