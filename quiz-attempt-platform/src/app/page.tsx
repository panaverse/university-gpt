import { Poppins } from "next/font/google";

import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { LoginButton } from "@/components/auth/login-button";
import { RegisterButton } from "@/components/auth/register-button";
import { BackgroundGradientAnimation } from "@/components/framer/background-gradient-animation";

const font = Poppins({
  subsets: ["latin"],
  weight: ["600"],
});

export default async function Home() {
  return (
      <BackgroundGradientAnimation>
        <div className="absolute z-50 inset-0 flex items-center justify-center text-white font-bold px-4 pointer-events-none text-3xl text-center md:text-4xl lg:text-7xl">
          <div className="space-y-6 text-center p-12 py-20 border-zinc-500 m-2 bg-gradient-to-b from-zinc-100 to to-blue-300/50 shadow-2xl rounded-lg">
            <h1
              className={cn(
                "text-4xl md:text-6xl font-semibold text-gray-700 drop-shadow-md inline-block transition-transform group-hover:translate-x-1 motion-reduce:transform-none",
                font.className
              )}
            >
              🔐 Enjoy Quizzes, Unlock Your Potential
            </h1>
            <p className="text-gray-500 text-lg">
              Get Ready to level up with another fun and engaging assessment
            </p>
            <div className="flex w-full justify-center space-x-2 md:space-x-6 pointer-events-auto">
              <LoginButton asChild>
                <Button variant="secondary" size="lg">
                  Sign in
                </Button>
              </LoginButton>
              <RegisterButton asChild>
                <Button variant="secondary" size="lg">
                  Register
                </Button>
              </RegisterButton>
            </div>
          </div>
        </div>
      </BackgroundGradientAnimation>
  );
}
