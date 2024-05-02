import { NextRequest, NextResponse } from "next/server"
import { redirect } from "next/navigation";
import { auth } from "@/lib/auth";


export async function POST(req: NextRequest) {

    try {
        /***** REQUIRED  BODY ******/
        const body = await req.json()
        console.log("[DATA]API_ROUTE_SAVE_ANSWER", body);

        const session = await auth();
        if (!session) {
          console.log("[session] No cookies. Redirecting...");
          redirect("/login");
        }

        const accessToken = session.access_token;

        // Send Data in JSON Format
        const get_quiz_attempt = await fetch(`${process.env.QUIZ_ATTEMPT_ASSESMENT_URL}/api/v1/answersheet/answer_slot/save`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${accessToken}`,
            },
            body: JSON.stringify({
                "quiz_answer_sheet_id": body.quiz_answer_sheet_id,
                "question_id": body.question_id,
                "question_type": body.question_type,
                "selected_options_ids": body.selected_options_ids
            }),
            cache: "no-store",
        });

        const response = await get_quiz_attempt.json();

        console.log("[SUCCESS]API_ROUTE_SAVE_ANSWER", get_quiz_attempt.status, get_quiz_attempt.statusText, response);

        return NextResponse.json(response)

     
    }
    catch (err) {
        console.error("[ERROR]:API_ROUTE_SAVE_ANSWER", err)
        return NextResponse.json({ success: false, message: "Api Call Failed", error: (err as string).toString() })
    }
}
