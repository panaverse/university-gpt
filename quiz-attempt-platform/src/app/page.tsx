import { Poppins } from "next/font/google";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { LoginButton } from "@/components/auth/login-button";
import { RegisterButton } from "@/components/auth/register-button";

const font = Poppins({
  subsets: ["latin"],
  weight: ["600"]
})

export default async function Home() {
  
  return (
    <main className="flex h-screen flex-col items-center justify-center border-gray-300 bg-gradient-to-b from-zinc-200 to to-blue-200/50 pb-6 pt-8 backdrop-blur-2xl ">
      <div className="space-y-6 text-center ">
        <h1 className={cn(
          "text-6xl font-semibold text-gray-700 drop-shadow-md inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none",
          font.className,
        )}>
          🔐 Assessment Platform
        </h1>
        <p className="text-gray-500 text-lg">
          Get Ready to level take your next assessment
        </p>
        <div className="flex w-full justify-center space-x-2">
          <LoginButton  asChild>
            <Button variant="secondary" size="lg">
              Sign in
            </Button>
          </LoginButton>
          <RegisterButton  asChild>
            <Button variant="secondary" size="lg">
              Register
            </Button>
          </RegisterButton>
        </div>
      </div>
    </main>
  )
}
