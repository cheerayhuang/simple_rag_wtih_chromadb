#import mysql.connector
import chromadb
import logging

from chromadb.utils import embedding_functions
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from langchain.text_splitter import CharacterTextSplitter

from chain_util import get_text_chunks
from settings import Settings

logging.basicConfig(
    datefmt=Settings.LOG_DATE_FORMAT,
    level=logging.INFO,
    format=Settings.LOG_FORMAT,
)
_log = logging.getLogger('db')

_default_ef = embedding_functions.DefaultEmbeddingFunction()


class _DefChromaEmbeddingsFunc(Embeddings):

  def __init__(self,ef):
    self._ef = ef

  def embed_documents(self,texts):
    return self._ef(texts)

  def embed_query(self, query):
    return self._ef([query])[0]


class DBMapper:

    def __init__(self, col_name=Settings.DEFAULT_COLLECTION):
        self._client = chromadb.PersistentClient(
            path=Settings.VECTOR_DB_PATH,
            #settings=chromadb.config.Settings(allow_reset=True),
        )

        self._col_name = col_name

        """
        col = self._client.get_or_create_collection(
            self._col_name,
            embedding_function=_default_ef,
        )
        """

        self._db = Chroma(
            client=self._client,
            collection_name=self._col_name,
            embedding_function=_DefChromaEmbeddingsFunc(_default_ef),
        )

        self._test_db = Chroma(
            client=self._client,
            collection_name="tests",
            embedding_function=_DefChromaEmbeddingsFunc(_default_ef),
        )

        self._retriever = self._db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={'score_threshold': 0.65, 'k': 3},
        )

        self._init_test()


    def _init_test(self):
        _log.info('chromadb init successful, testing beging...')

        docs = ['hello', 'hi', 'how', 'why', 'whether']
        for doc in docs:
            self.save_doc(
                doc,
                file_name=f'{doc}.txt',
                is_test=True,
            )

        _log.info(f'{self._test_db.similarity_search_with_relevance_scores("hello", k=5)}')

        try:
            self._client.delete_collection('tests')
        except ValueError:
            pass

        _log.info('testing end.')


    def open(self, col_name=Settings.DEFAULT_COLLECTION):
        self._col_name = col_name
        self._db = Chroma(
            client=self._client,
            collection_name=self._col_name,
            embedding_function=_DefChromaEmbeddingsFunc(_default_ef),
        )
        self._retriever = self._db.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={'score_threshold': 0.65, 'k': 3},
        )


    def close(self, col_name=Settings.DEFAULT_COLLECTION):
        try:
            if self._col_name != '':
                self._client.delete_collection(self._col_name)
            else:
                self._client.delete_collection(col_name)
        except ValueError:
            pass
        finally:
            self._db = None
            self._retriever = None
            self._col_name = ''


    def destroy(self):
        pass


    def filter_by_file(self, f_name):
        return self.query('', {'f_name': f_name})


    def query(self, q, f, k=100):
        #results = vector_store.similarity_search(query="thud",k=1)
        res = self._db.similarity_search(
            query=q, k=k,filter=f)

        for doc in res:
            _log.info(doc)


    def save_doc(self, content, file_name, is_test=False):
        #col = self._client.get_collection(self._defualt_col_name)
        chunks, chunks_ids = get_text_chunks(content)
        metas = [{'f_name': f'{file_name}'} for _ in range(len(chunks))]

        db = self._test_db if is_test else self._db
        if db is None:
            raise ValueError

        db.add_texts(
            texts=chunks,
            ids=chunks_ids,
            metadatas=metas,
        )

        _log.info(f'save doc successful, the total of chunks: {len(chunks)}, the first&last chunk info:\n\t'
            f'len: {len(chunks[0])}, id: {chunks_ids[0]}, meta: {metas[0]}\n\t'
            f'len: {len(chunks[-1])}, id: {chunks_ids[-1]}, meta: {metas[-1]}')


    def as_retriever(self):
        return self._retriever


    def as_filter_by_file_retriever(self, f_name):
        return self._db.as_retriever(
            query='',
            search_type='similarity',
            search_kwargs={
                'k': 100,
                #'query': '',
                'filter': {
                    'f_name': f_name,
                },
            }
        )


db = DBMapper()

if __name__ == '__main__':
    #print(_default_ef(['hello']))
    pass

"""
def connect_to_mysql():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="chain"
    )
    return db


def select(agent_no):
    db = connect_to_mysql()
    cursor = db.cursor()

    cursor.execute("select * from chain where agent_no=%s", (agent_no,))
    result = cursor.fetchone()
    cursor.close()
    db.close()
    return result


def save(agent_no, text):
    db = connect_to_mysql()
    cursor = db.cursor()

    cursor.execute("insert into chain (agent_no, text) values (%s, %s)", (agent_no, text))
    cursor.close()
    db.close()


print(select("123")[0])
"""
