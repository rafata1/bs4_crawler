import base64

from bs4 import BeautifulSoup
from PIL import Image
import requests
from io import BytesIO

from requests import RequestException


def resize_image(img_url, max_width=620, timeout=5):
    try:
        response = requests.get(img_url, timeout=timeout)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))

        # Set a maximum width for the image
        width_percent = (max_width / float(img.size[0]))
        new_height = int((float(img.size[1]) * float(width_percent)))
        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)

        # Convert the image to a data URL
        buffered = BytesIO()
        img.save(buffered, format="JPEG")

        # Encode the image data using base64
        img_data_url = f"data:image/jpeg;base64,{base64.b64encode(buffered.getvalue()).decode('utf-8')}"

        return img_data_url
    except RequestException as e:
        print(f"Error or timeout resizing image: {e}")
        return img_url



def merge_to_wordpress_post(html_content, max_image_width=620):
    # Parse the HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Create WordPress post content
    wordpress_content = ""

    for element in soup.find_all(['p', 'img']):
        if element.name == 'p':
            # Append paragraphs with <p> tags
            wordpress_content += f'<p>{element.text}</p>'
        elif element.name == 'img':
            # Resize the image and append with <img> tags
            img_url = element.get('data-src') or element['src']
            resized_img_data_url = resize_image(img_url, max_image_width)

            if resized_img_data_url:
                alt_text = element.get('alt', '')
                wordpress_content += f'<img src="{resized_img_data_url}" alt="{alt_text}">'

    return wordpress_content


# Example HTML content
html_content = '''
<div class="entry-content">

		<div class="code-block code-block-1" style="margin: 8px auto; text-align: center; display: block; clear: both;">
<style> #M929229ScriptRootC1561356 { min-height: 300px; }</style> 
 <!-- Composite Start --> 
     <div id="M929229ScriptRootC1561356_03192" style="min-height:auto !important;"> 
     </div> 
     <script src="https://jsc.mgid.com/n/e/newssportvip.com.1561356.js" async=""> 
     </script> 
 <!-- Composite End --> 
 </div>
<p><img decoding="async" src="https://s.yimg.com/ny/api/res/1.2/hY08gQtQYS2ZeJ16o6B.ig--/YXBwaWQ9aGlnaGxhbmRlcjt3PTE4MDA7aD05NjA7Y2Y9d2VicA--/https://media.zenfs.com/en/wttv_articles_599/de80225bba15a4b1d38fd155a9afcd97"></p>
<p>EDINBURGH, Ind. – A large fire broke out Friday evening at a recycling facility in Edinburgh, Indiana.</p>
<p>According to the Edinburgh Police Department, police and fire crews were dispatched to the Group Metal Recycling Facility in the 100 block of North Holland Street at around 5:35 p.m. Friday evening.</p><div id="M929229ScriptRootC1571398_00fed"></div><script src="https://jsc.mgid.com/n/e/newssportvip.com.1571398.js" async=""></script>
<p>Crews found the building engulfed in flames when they arrived on scene. Police say multiple agencies were dispatched to assist the Edinburgh Fire Department due to the nature of the fire.</p>
<div class="caas-da">
<div id="sda-INARTICLE"><img decoding="async" src="https://www.wishtv.com/wp-content/uploads/2024/01/Edinburgh-fire-4-e1705113319269.jpg"></div>
</div>
<p>It took fire crews approximately two hours to get the fire under control due to the business having a lot of vehicle parts, oil and propane tanks throughout the building.</p>
<p><img decoding="async" src="https://cbs4indy.com/wp-content/uploads/sites/22/2024/01/Fire-scene-1.jpg"></p><div id="M929229ScriptRootC1571398_0900f"></div><script src="https://jsc.mgid.com/n/e/newssportvip.com.1571398.js" async=""></script>
<p></p><div class="code-block code-block-2" style="margin: 8px 0; clear: both;">
<!-- Composite Start --> <div id="M929229ScriptRootC1561362_0ec3d"> </div> <script src="https://jsc.mgid.com/n/e/newssportvip.com.1561362.js" async=""> </script> <!-- Composite End --></div>
<!-- AI CONTENT END 1 -->
</div>
'''

# Create WordPress post content with resized images
wordpress_post_content = merge_to_wordpress_post(html_content)

output_file_path = "wordpress_post.html"
with open(output_file_path, "w", encoding="utf-8") as file:
    file.write(wordpress_post_content)

print(f"WordPress post content saved to {output_file_path}")
