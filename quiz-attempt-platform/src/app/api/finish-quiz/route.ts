import { NextRequest, NextResponse } from "next/server"
import { redirect } from "next/navigation";
import { auth } from "@/lib/auth";


export async function PATCH(req: NextRequest) {

    try {
        /***** REQUIRED  BODY ******/
        const body = await req.json()
        console.log("[DATA]API_ROUTE_FINISH_QUIZ", body);

        // Get quiz_answer_sheet_id from body
        const quiz_answer_sheet_id = body.quiz_answer_sheet_id;

        const session = await auth();
        if (!session) {
          console.log("[session] No cookies. Redirecting...");
          redirect("/login");
        }

        const accessToken = session.access_token;

        // Send Data in JSON Format
        const get_quiz_attempt = await fetch(`${process.env.QUIZ_ATTEMPT_ASSESMENT_URL}/api/v1/answersheet/${quiz_answer_sheet_id}/finish`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${accessToken}`,
            },
            cache: "no-store",
        });

        const response = await get_quiz_attempt.json();

        console.log("[SUCCESS]API_ROUTE_FINISH_QUIZ", get_quiz_attempt.status, get_quiz_attempt.statusText, response);

        return NextResponse.json(response)

    }
    catch (err) {
        console.error("[ERROR]:API_ROUTE_FINISH_QUIZ", err)
        return NextResponse.json({ success: false, message: "Api Call Failed", error: (err as string).toString() })
    }
}
