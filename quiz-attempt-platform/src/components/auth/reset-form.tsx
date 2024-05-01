"use client";

import * as z from "zod";
import { useForm } from "react-hook-form";
import { useState, useTransition } from "react";
import { useRouter } from "next/navigation";
import { zodResolver } from "@hookform/resolvers/zod";

import { ResetSchema } from "@/schemas";
import { Input } from "@/components/ui/input";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { CardWrapper } from "@/components/auth/card-wrapper";
import { Button } from "@/components/ui/button";
import { FormError } from "@/components/form-error";
import { FormSuccess } from "@/components/form-success";
import { reset } from "@/global-actions/reset-password";
import { DEFAULT_RESET_REDIRECT } from "@/lib/routes";
import { useToast } from "../ui/use-toast";
import { ToastAction } from "../ui/toast";


export const ResetForm = () => {


  const [error, setError] = useState<string | undefined>("");
  const [success, setSuccess] = useState<string | undefined>("");
  const [isPending, startTransition] = useTransition();
  const router = useRouter()
  const { toast } = useToast()

  const form = useForm<z.infer<typeof ResetSchema>>({
    resolver: zodResolver(ResetSchema),
    defaultValues: {
      email: "",
    },
  });

  const onSubmit = (values: z.infer<typeof ResetSchema>) => {
    setError("");
    setSuccess("");    

    startTransition(() => {
        reset(values)
        .then((data) => {
            setError(data.error);   
            setSuccess(data.success);
          if (data?.error) {
            form.reset();
            toast({
              title: "Reset Password Request Failed",
              description: data.error,
              variant: "destructive",
              action: (
                <ToastAction altText="Dismiss">Dismiss</ToastAction>
               )
            })
            
          }

          if (data?.success) {
            form.reset();
            setSuccess(data.success);
            toast({
              title: "Password Reset Email Sent",
              description: data.success,
              action: (
               <ToastAction altText="Close">Close</ToastAction>
              ),
            })
            router.push(DEFAULT_RESET_REDIRECT );
          }
        })
    });
  };

  return (
    <CardWrapper
      headerLabel="Reset Password"
      backButtonLabel="Don't have an account?"
      backButtonHref={ "/register"}
    >
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          <div className="space-y-4">
              <>
                <FormField
                  control={form.control}
                  name="email"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Enter your Email</FormLabel>
                      <FormControl>
                        <Input
                          {...field}
                          disabled={isPending}
                          placeholder="johndoe@example.com"
                          type="email"
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </>
          </div>
          <FormError message={error} />
          <FormSuccess message={success}  />
          <Button disabled={isPending} type="submit" className="w-full">
            {"Reset Password"}
          </Button>
        </form>
      </Form>
    </CardWrapper>
  );
};
