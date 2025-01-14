from transformers import pipeline
from typing import List


class SummarizationModel:
    """Summarization model using Hugging Face pipeline."""

    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    @staticmethod
    def split_text(text: str, max_tokens: int = 1024) -> List[str]:
        """
        Split the text into smaller chunks within the max token limit.

        Args:
            text (str): The text to split.
            max_tokens (int): The maximum token length for each chunk.

        Returns:
            List[str]: List of text chunks.
        """
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0

        for word in words:
            current_length += len(word) + 1  # Adding 1 for the space
            if current_length > max_tokens:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = len(word) + 1
            else:
                current_chunk.append(word)

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def summarize(self, text: str, max_length: int = 130, min_length: int = 30) -> str:
        """
        Summarize the input text.

        Args:
            text (str): Input text to summarize.
            max_length (int): Maximum length of summary.
            min_length (int): Minimum length of summary.

        Returns:
            str: Summarized text.
        """
        tokenizer = self.summarizer.tokenizer
        token_count = len(tokenizer.encode(text, return_tensors="pt")[0])
        #token_count = len(self.summarizer.tokenizer.encode(text))

        if token_count <= 1024:
            summary = self.summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
            return summary[0]["summary_text"]
        else:
            chunks = self.split_text(text, max_tokens=1024)
            summaries = [self.summarize(chunk, max_length=max_length, min_length=min_length) for chunk in chunks]
            return " ".join(summaries)


#text = "REVIEWS OF EDUCATIONAL MATERIAL\nAlan Jay Schwartz, M.D., M.S.Ed., Editor\nof practice, as well as provides insightful clinical pearls in\nThe Basics of Anesthesia, 7th Edition. Edited by\neach section.\nManuel Pardo, M.D., and Ronald D. Miller, M.D., M.S.\nThe evolution of our specialty and the changing context\nNew York, Elsevier, 2017. Pages: 936. Price: $95.99.\nof anesthesiology practice is reflected in this new edition.\nMiller\u2019s Anesthesia Review, 3rd Edition. Written\nThere is an expanded and improved section on outpatient\nby Lorraine M. Sdrales, M.D., and Ronald D. Miller,\nsedation, an updated section on hyperalgesia and the opi-\nM.D., M.S. New York, Elsevier, 2017. Pages: 544.\noid crisis in the pain chapter, and a beautifully organized\nPrice: $87.36.\ntrauma section. Chapter 12 is a welcomed addition, pro-\nIn the world of anesthesia, very few textbooks resonate viding an outstanding summary of the current state of\nDownloaded\nwith anesthesiologists the way that The Basics of Anesthesia the controversial topic of anesthetic neurotoxicity. The\ndoes. This is the 7th edition of this classic, and the timing of addition of the \u201cHuman Induced and Natural Disasters\u201d\nthis edition coincides with release of an update of the com- chapter sheds light on important aspects of our current\nfrom\npanion study guide, Miller\u2019s Anesthesia Review. The book geopolitical realities. In the context of the anesthesiolo-\nhttp://pubs.asahq.org/anesthesiology/article-pdf/129/6/1194/382132/20181200_0-00039.pdf\nhonors the 33-yr stewardship of Dr. Miller, and ushers in gist as the \u201cperioperative physician,\u201d the text highlights the\na changing of the guard with Dr. Pardo assuming the role importance of anesthesiologists as in-hospital physicians\nof lead editor. One will quickly notice the growth and far whose clinical skills and leadership provide value to the\nreaching collection of authors that have contributed to this system as a whole. The \u201cPalliative Care\u201d and \u201cSleep Medi-\nversion; there are a total of 87 authors in this edition. There cine and Anesthesia\u201d chapters are brief introductions to\nare many familiar names, with the addition of new authors worlds not very familiar to most; providing succinct, yet\nadding a unique and updated perspective. complete, overviews of new subspecialties that are evolving\nAt first glance, this book looks like previous versions. and gaining importance in our specialty. One of the most\nThe organization of the book is what we have come to innovative chapters is \u201cNew Models of Anesthesia Care:\nexpect. For an introductory book it is robust: 936 pages. Perioperative Medicine, the Perioperative Surgical Home,\nOn further inspection, the reader will immediately notice and Population Health,\u201d encompassing new initiatives that\nthat this edition is much more visually pleasing, with bet- provide value beyond the operating room, with a focus on\nter illustrations and important information more usefully the perioperative surgical home. For someone new to the\nhighlighted. Each chapter is organized better than in previ- field, it is an excellent introduction to the landscape of\nous editions, which leads to improved flow overall. Gone health care and the anesthesiologist\u2019s future and role in this\nis the history chapter. Gone are the numerous appendices rapidly evolving world.\nand \u201cPlease refer to\u2026\u201d comments. Although this is touted The negatives in this book are few, and most are related to\nas a basics book, there is nothing basic about this book; it the electronic version of the text. The eBook, while adding\nis dense with information and, while easy to read, it is not convenient access, does not offer anything additive or inno-\na quick read. vative. In fact, it is essentially a digital copy of the hardcopy\nThe sections of the book are organized similarly to previ- book. While there is the ability to highlight text and save by\nguest\nous editions. Most of the information in the basic science \u201cnotes,\u201d the search functionality is essentially a word search.\nand pharmacology sections remain the same, but rather than On the whole, the regional section was perhaps the most dis- on\n18\npresenting a dry litany of scientific fact, there is a concerted appointing. Both the paper and digital versions would have February\neffort to relate the information in a more clinical fashion. benefited from a more through catalogue and description of\nThe detailed introduction gives the topic a clinical focus, and basic blocks. This could have been an area where the digital 2021\nin some sections a brief historical perspective is provided to version distinguished itself with an enhanced library of digi-\nmake up for the loss of the chapter on anesthesia history. tal images or video clips.\nThe addition of a physical diagnoses segment in each chapter As a companion to this text, Drs. Sdrales and Miller offer\nis welcome, providing more opportunities to tie the scien- Miller\u2019s Anesthesia Review, in its 3rd edition. It again has a\ntific facts to clinical practice. The pharmacology section is familiar format to previous versions and is laid out in chap-\nalso enhanced with additional focus on the pharmacologic ters that match the text. It serves as a very thorough study\nimplications of obesity and advanced age. The updates to guide when used in conjunction with the textbook, with\ncommon practice, with the exclusion of halothane from open ended questions and detailed explanations that high-\nclinical practice and the addition of newer drugs like sugam- light key points. For trainees looking for help in preparation\nmadex, brings the text into alignment with the current state for the American Board of Anesthesiology Part 1A Exam,\nthis book provides an excellent synopsis of the fundamen-\ntals; however, this is not the traditional test prep book with\nmultiple choice questions. The use of open ended questions,\nCopyright \u00a9 2018, the American Society of Anesthesiologists, Inc. Wolters\nKluwer Health, Inc. All Rights Reserved. Anesthesiology 2018; 129:1194-5 coupled with the discussions that tie basic science concepts\nAnesthesiology, V 129 \u2022 No 6 1194 December 2018\nCopyright \u00a9 2018, the American Society of Anesthesiologists, Inc. Wolters Kluwer Health, Inc. Unauthorized reproduction of this article is prohibited.\n<zdoi;10.1097/ALN.0000000000002432>"
#summarizer = SummarizationModel()
#summary = summarizer.summarize(text)
#print("Final Summary:\n", summary)
##TODO: put max length = max length of input