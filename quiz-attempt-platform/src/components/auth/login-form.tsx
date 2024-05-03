"use client";

import * as z from "zod";
import { useForm } from "react-hook-form";
import { useState, useTransition } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { zodResolver } from "@hookform/resolvers/zod";

import { LoginSchema } from "@/schemas";
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
import { login } from "@/global-actions/login";
import { DEFAULT_LOGIN_REDIRECT } from "@/lib/routes";
import { useToast } from "../ui/use-toast";
import { ToastAction } from "../ui/toast";
import Link from "next/link";


export const LoginForm = () => {
  const searchParams = useSearchParams();

  // Get all the query params
  const redirect_uri = searchParams.get("redirect_uri");
  const client_id = searchParams.get("client_id");
  const response_type = searchParams.get("response_type");
  const scope = searchParams.get("scope");
  const state = searchParams.get("state");

  const queryParams = `?redirect_uri=${redirect_uri}` + `&state=${state}` + `&response_type=${response_type}` + `&client_id=${client_id}` + `&scope=${scope}`

  let callbackUrl: string | null = null

  if (redirect_uri) {
    callbackUrl = `/dashboard${queryParams}`
  }

  const urlError =
    searchParams.get("error") === "OAuthAccountNotLinked"
      ? "Email already in use with different provider!"
      : "";

  const [error, setError] = useState<string | undefined>("");
  const [success, setSuccess] = useState<string | undefined>("");
  const [isPending, startTransition] = useTransition();
  const router = useRouter()
  const { toast } = useToast()

  const form = useForm<z.infer<typeof LoginSchema>>({
    resolver: zodResolver(LoginSchema),
    defaultValues: {
      email: "",
      password: "",
    },
  });

  const onSubmit = (values: z.infer<typeof LoginSchema>) => {
    setError("");
    setSuccess("");    

    startTransition(() => {
      login(values)
        .then((data) => {
          if (data?.error) {
            setError(data.error);
            toast({
              title: "Login Failed",
              description: data.message ? data.message : "Request Failed, Try Again",
              duration: 2000,
              action: (
                <ToastAction altText="Dismiss" >Dismiss</ToastAction>
               )
            })
            form.reset();
          }

          if (data?.success) {
            form.reset();
            setSuccess(data.success);
            toast({
              title: "Login Success",
              description: data.message ? data.message : "Welcome to Cax AI",
              duration: 2000,
              action: (
               <ToastAction altText="Close">Close</ToastAction>
              ),
            })
            router.push(callbackUrl || DEFAULT_LOGIN_REDIRECT );
          }
        })
    });
  };

  return (
    <CardWrapper
      headerLabel="Welcome back"
      backButtonLabel="Don't have an account?"
      backButtonHref={redirect_uri ? `/register${queryParams}` : "/register"}
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
                      <FormLabel>email</FormLabel>
                      <FormControl>
                        <Input
                          {...field}
                          disabled={isPending}
                          placeholder="johndoe"
                          type="text"
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="password"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Password</FormLabel>
                      <FormControl>
                        <Input
                          {...field}
                          disabled={isPending}
                          placeholder="******"
                          type="password"
                        />
                      </FormControl>
                      <Button
                        size="sm"
                        variant="link"
                        asChild
                        className="px-0 font-normal"
                      >
                        <Link href="/reset">Forgot password?</Link>
                      </Button>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </>
          </div>
          <FormError message={error || urlError} />
          <FormSuccess message={success}  />
          <Button disabled={isPending} type="submit" className="w-full">
            {"Login"}
          </Button>
        </form>
      </Form>
    </CardWrapper>
  );
};
