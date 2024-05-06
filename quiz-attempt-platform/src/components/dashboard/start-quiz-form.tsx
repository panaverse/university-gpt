"use client";

import * as z from "zod";
import { useForm } from "react-hook-form";
import { useState, useTransition } from "react";
import { useRouter } from "next/navigation";
import { zodResolver } from "@hookform/resolvers/zod";

import { StartQuizSchema } from "@/schemas/quiz";
import { Input } from "@/components/ui/input";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Button } from "@/components/ui/button";
import { FormError } from "@/components/form-error";
import { FormSuccess } from "@/components/form-success";
import { DEFAULT_QUIZ_ATTEMPT_REDIRECT } from "@/lib/routes";
import { useToast } from "../ui/use-toast";
import { ToastAction } from "../ui/toast";
import { startQuizAction } from "@/global-actions/start-quiz";
import { useQuizStore } from "@/stores/quiz-store";

export const StartQuizForm = () => {
  const [error, setError] = useState<string | undefined>("");
  const [success, setSuccess] = useState<string | undefined>("");
  const [isPending, startTransition] = useTransition();
  const router = useRouter();
  const { toast } = useToast();
    // Set the fetched quiz data in Zustand store
  const { setQuizData, clearQuizData } = useQuizStore.getState();
    
  const form = useForm<z.infer<typeof StartQuizSchema>>({
    resolver: zodResolver(StartQuizSchema),
    defaultValues: {
      quizKey: "",
      quizId: 0,
    },
  });

  const onSubmit = (values: z.infer<typeof StartQuizSchema>) => {
    setError("");
    setSuccess("");

    startTransition(() => {
        startQuizAction(values).then((data) => {
            setError(data.error);
            setSuccess(data.success);
            if (data?.error) {
            form.reset();
            toast({
                title: "Quiz Attempt Failed",
                description: data.error,
                variant: "destructive",
                duration: 2000,
                action: <ToastAction altText="Dismiss">Dismiss</ToastAction>,
            });
            }

            if (data?.success) {
              clearQuizData();
              setQuizData(data?.data);
              form.reset();
              setSuccess(data.success);
              toast({
                  title: "Quiz Attempt Started!",
                  description: data.success,
                  duration: 2000,
                  action: <ToastAction altText="Close">Close</ToastAction>,
              });
              router.push(DEFAULT_QUIZ_ATTEMPT_REDIRECT);
            }
      });
    });
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="flex flex-col items-center justify-center space-y-4">
        <div className="flex flex-col md:flex-row items-center justify-center gap-4">
          <FormField
            control={form.control}
            name="quizKey"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Enter Quiz Key</FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    disabled={isPending}
                    placeholder="PoetryQuiz"
                    type="string"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
           <FormField
            control={form.control}
            name="quizId"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Enter Quiz Id</FormLabel>
                <FormControl>
                  <Input
                    {...field}
                    disabled={isPending}
                    placeholder="123"
                    type="number"
                    value={field.value === 0 ? "0" : field.value}
                    onChange={(e) => field.onChange(parseInt(e.target.value))}          
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

        </div>

        <p className="text-sm text-gray-500 dark:text-gray-400">
          Enter the quiz key and Id provided by your instructor to start the quiz.
        </p>

        <FormError message={error} />
        <FormSuccess message={success} />
        <Button disabled={isPending} type="submit" className="w-auto px-16">
          {"Start Quiz"}
        </Button>
      </form>
    </Form>
  );
};
