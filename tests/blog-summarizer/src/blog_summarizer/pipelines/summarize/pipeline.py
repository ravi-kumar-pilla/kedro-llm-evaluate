from .nodes import summarize_blog_posts
from kedro.pipeline import Pipeline, node

def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline([
        node(
            func=summarize_blog_posts,
            inputs="raw_blog_posts",
            outputs="summarized_blog_posts",
            name="summarize_node"
        )
    ])
