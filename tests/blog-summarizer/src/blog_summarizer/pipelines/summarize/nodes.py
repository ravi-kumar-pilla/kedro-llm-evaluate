from kedro_llm_evaluate.tracing import trace_llm
import ollama

def summarize_blog_posts(blog_posts_df) -> list[dict]:
    summaries = []   
    blog_posts = blog_posts_df.to_dict(orient="records")  # convert to list of dicts
    for post in blog_posts:
        prompt = (
            "Summarize the following blog post into a concise version that's a 1 to 5 minute read:\n\n"
            + post["content"]
        )

        with trace_llm(model="llama3", prompt=prompt) as span:
            response = ollama.chat(
                model="llama3",
                messages=[
                    {"role": "system", "content": "You are a helpful summarizer."},
                    {"role": "user", "content": prompt}
                ],
                options={
                    "temperature": 0.7,
                    "num_predict": 2048
                }
            )
            
            summary = response.message.content
            
            # Attach the output onto the span so end_trace can pick it up:
            span.span_output = summary

            summaries.append({
                "title": post["title"],
                "summary": summary
            })

    return summaries
