from groq import Groq
from kedro_llm_evaluate.tracing import trace_llm
import os

# Initialize Groq client once
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def summarize_blog_posts(blog_posts_df) -> list[dict]:
    summaries = []   
    blog_posts = blog_posts_df.to_dict(orient="records")  # convert to list of dicts
    for post in blog_posts:
        prompt = (
            "Summarize the following blog post into a concise version that's a 1 to 5 minute read:\n\n"
            + post["content"]
        )

        with trace_llm(model="llama3-8b-8192", prompt=prompt) as span:
            response = groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are a helpful summarizer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2048
            )
            summary = response.choices[0].message.content
            
            # Attach the output onto the span so end_trace can pick it up:
            span.span_output = summary

            summaries.append({
                "title": post["title"],
                "summary": summary
            })

    return summaries
