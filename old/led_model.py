import os
import time
from datetime import timedelta
from textsum.summarize import Summarizer

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"


# slower model: 0:03:14.094656
def led_summarization(text):
    # starttime = time.perf_counter()
    model_name = "pszemraj/led-base-book-summary"

    summarizer = Summarizer(
        model_name_or_path=model_name,  # you can use any Seq2Seq model on the Hub
        token_batch_length=4096,  # tokens to batch summarize at a time, up to 16384
    )
    try:
        out_str = summarizer.summarize_string(text)
    except AttributeError:
        out_str = summarizer(text)

    # duration = timedelta(seconds=time.perf_counter() - starttime)
    # print('Summarization took: ', duration)
    return out_str

# text = """In the early days of humanity, survival was the primary concern for people, and the idea of leisure or entertainment did not exist in the same way it does today. People lived in small, tight-knit communities, relying heavily on agriculture, hunting, and gathering to feed their families. Tools and resources were scarce, and each individual had to contribute to the well-being of the group in some way. There was little time for frivolous pursuits, as every moment was spent ensuring that basic needs were met.
# As civilization evolved, so too did the nature of human existence. Over centuries, people began to establish more permanent settlements, and with these new forms of society came the concept of work as well as leisure. Societies began to specialize in different crafts, trades, and industries, allowing for the creation of goods beyond what was necessary for survival. People began to trade, exchanging goods and services that enhanced their lives and provided new opportunities. The concept of art emerged, with paintings, sculptures, and music becoming ways to express beauty, culture, and emotion.
# The Industrial Revolution marked a turning point in human history. The advent of machines and mass production changed the dynamics of work and life. People moved from rural areas to urban centers in search of employment in factories, where they worked long hours for relatively low wages. At the same time, the rise of industry led to the creation of wealth and the growth of a middle class. With this newfound wealth came an increase in leisure time, and entertainment began to take on new forms. Theatres, concerts, and other forms of public entertainment became popular, as people sought ways to escape the monotony of factory work.
# Over time, technology continued to advance, leading to even more changes in how people spent their time. The invention of television in the 20th century revolutionized entertainment, bringing movies, news, and sports directly into people's homes. People could now relax and enjoy their favorite programs without having to leave the comfort of their homes. In the digital age, the internet has further transformed how we engage with entertainment and information. Social media, streaming services, and video games have become central to modern life, offering countless ways to relax, socialize, and learn.
# The rise of the digital age has brought about dramatic shifts in human behavior. With access to the internet, people can now connect with others from around the world in real-time. Social media platforms have created new ways for people to interact, share ideas, and build communities. The impact of these technological advancements is profound, as they have created new forms of social and cultural interaction. People no longer have to rely solely on physical communities; instead, they can participate in global networks of like-minded individuals.
# Despite the many advances in entertainment and technology, the question of how people should spend their leisure time remains an important one. As our lives become increasingly busy and filled with distractions, it is crucial to find ways to balance work and leisure. Many people struggle to disconnect from their devices and social media, finding themselves constantly plugged in, often at the expense of meaningful relationships and self-care. Some argue that the digital age has made it harder to relax and unwind, as constant notifications and the pressure to stay connected can lead to burnout.
# In contrast, others argue that technology has provided more opportunities than ever before to relax and enjoy ourselves. Streaming services offer endless entertainment options, video games provide immersive experiences, and social media allows people to stay in touch with friends and family regardless of geographical distance. The internet has made it easier than ever to access information, learn new skills, and explore different cultures. While it is true that technology can sometimes be overwhelming, it also has the potential to enrich our lives in countless ways.
# The future of leisure and entertainment will likely continue to evolve alongside advancements in technology. Virtual reality and augmented reality are just two examples of emerging technologies that could change the way we experience entertainment. These technologies promise to create more immersive and interactive experiences, allowing people to step into new worlds and engage with content in ways that were previously unimaginable. As artificial intelligence continues to develop, we may also see the rise of personalized entertainment experiences tailored to individual preferences and needs.
# As we look toward the future, it is important to consider how we can continue to enjoy leisure while maintaining a healthy balance in our lives. While technology offers many benefits, it is important to remember the value of offline activities like spending time in nature, reading a book, or simply sitting with loved ones. Leisure is not just about entertainment—it is about finding time to relax, recharge, and reflect. In a world that is increasingly fast-paced and digitally connected, taking time to disconnect and engage in meaningful activities will continue to be essential for our well-being.
# In conclusion, the evolution of leisure and entertainment reflects the broader changes in society and technology. From the early days of survival to the rise of industry, and now to the digital age, the ways in which people spend their time have shifted dramatically. As technology continues to advance, the opportunities for entertainment and relaxation will only continue to grow. However, it is essential to maintain a healthy balance between work and leisure in order to lead fulfilling lives. By finding ways to embrace technology while also valuing offline activities, we can create a future where both work and relaxation coexist harmoniously."""
# print(led_summarization(text))
# print(long_summarization(text))
