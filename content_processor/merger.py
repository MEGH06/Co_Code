from content_processor.summarizer import summarize_content
from content_processor.table_processor import filter_tables
from content_processor.image_processor import filter_images

def merge_content(content):
    """Merge and summarize content."""
    # Summarize text
    summarized_text = summarize_content(content["text"])
    consolidated_tables = filter_tables(content["tables"])
    consolidated_images = filter_images(content["images"])
    # Create functions separately for deciding tables and images

    return {
        "text": summarized_text,
        "tables": consolidated_tables,
        "images": consolidated_images
    }