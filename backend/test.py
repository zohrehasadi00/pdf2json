import io
import concurrent.futures
import pdfplumber
import fitz


def get_page_count_from_bytes(pdf_bytes):
    """Get the total number of pages from PDF bytes."""
    doc = fitz.open("pdf", io.BytesIO(pdf_bytes))
    page_count = doc.page_count
    doc.close()
    return page_count


def extract_text_from_page(pdf_bytes, page_number):
    """Extract text from a specific page using pdfplumber."""
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            page = pdf.pages[page_number - 1]
            text = page.extract_text() or ''
        return {'page_number': page_number, 'text': text}
    except Exception as e:
        print(f"Error extracting text from page {page_number}: {e}")
        return {'page_number': page_number, 'text': ''}


def extract_images_from_page(pdf_bytes, page_number):
    """Extract images from a specific page using PyMuPDF."""
    images = []
    doc = None
    try:
        doc = fitz.open("pdf", io.BytesIO(pdf_bytes))
        page = doc.load_page(page_number - 1)  # PyMuPDF uses 0-based index
        image_list = page.get_images()
        for img in image_list:
            xref = img[0]
            try:
                base_image = doc.extract_image(xref)
                if 'image' in base_image:
                    images.append(base_image['image'])
            except Exception as e:
                print(f"Error extracting image on page {page_number}: {e}")
    except Exception as e:
        print(f"Error processing images on page {page_number}: {e}")
    finally:
        if doc:
            doc.close()
    return {'page_number': page_number, 'images': images}


def process_text_extraction(pdf_bytes, max_workers=None):
    """Process all pages in parallel for text extraction."""
    page_count = get_page_count_from_bytes(pdf_bytes)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        args = [(pdf_bytes, pn) for pn in range(1, page_count + 1)]
        futures = [executor.submit(extract_text_from_page, *arg) for arg in args]
        text_results = []
        for future in concurrent.futures.as_completed(futures):
            text_results.append(future.result())
        text_results.sort(key=lambda x: x['page_number'])
    return text_results


def process_image_extraction(pdf_bytes, max_workers=None):
    """Process all pages in parallel for image extraction."""
    page_count = get_page_count_from_bytes(pdf_bytes)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        args = [(pdf_bytes, pn) for pn in range(1, page_count + 1)]
        futures = [executor.submit(extract_images_from_page, *arg) for arg in args]
        image_results = []
        for future in concurrent.futures.as_completed(futures):
            image_results.append(future.result())
        image_results.sort(key=lambda x: x['page_number'])
    return image_results


def process_pdf(pdf_path, max_workers=None):
    """Main function to process PDF and return combined results."""
    with open(pdf_path, 'rb') as f:
        pdf_bytes = f.read()

    text_results = process_text_extraction(pdf_bytes, max_workers)
    image_results = process_image_extraction(pdf_bytes, max_workers)

    merged_results = []
    for text_dict, image_dict in zip(text_results, image_results):
        merged_dict = {
            'page_number': text_dict['page_number'],
            'text': text_dict['text'],
            'images': image_dict['images']
        }
        merged_results.append(merged_dict)

    return merged_results
