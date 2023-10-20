package io.github.fededa.lucenecustomhandler;

import io.github.fededa.exceptions.EmptyUserInputException;
import io.github.fededa.inputhandler.InputHandlerInterface;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.CharArraySet;
import org.apache.lucene.analysis.core.WhitespaceAnalyzer;
import org.apache.lucene.analysis.miscellaneous.PerFieldAnalyzerWrapper;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.codecs.Codec;
import org.apache.lucene.codecs.simpletext.SimpleTextCodec;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

public class LuceneCustomHandler implements LuceneCustomHandlerInterface{

    private final InputHandlerInterface ih;

    public LuceneCustomHandler(InputHandlerInterface _ih){
        ih=_ih;
    }
    @Override
    public void printHelloWorldtTest() {
        System.out.println("Hello World from Lucene Custom Library");
    }

    @Override
    public TopDocs runHw_2(QueryParser parser, List<Document> docsList) throws Exception{
        Path path = Paths.get("target/idx0");
        // Lucene's index is stored here
        try (Directory directory = FSDirectory.open(path)) {

            // Opening the file-system directory for the Lucene index.
            indexDocs(directory, new SimpleTextCodec(), docsList);

            // Opens a reader for the Lucene index; this is read-only and prevents modifications.
            try (IndexReader reader = DirectoryReader.open(directory)) {
                String userInput = ih.readUserInput("What are you looking for today?\n");
                if(userInput.isEmpty()) throw new EmptyUserInputException();
                //QueryParser parser = new QueryParser("titolo", new WhitespaceAnalyzer());
                // Builds query
                Query query = parser.parse(userInput);
                // Allows searching within Lucene's index
                IndexSearcher searcher = new IndexSearcher(reader);
                TopDocs results = searcher.search(query,10);
                for (ScoreDoc scoreDoc : results.scoreDocs) {
                    Document doc = searcher.doc(scoreDoc.doc);
                    System.out.println("doc"+scoreDoc.doc + ":"+ doc.get("titolo") + " (" + scoreDoc.score +")");
                }
                return results;
            } finally {
                directory.close();
            }
        }
    }

    /**
     *  Initializes and configures Lucene IndexWriter and indexes docs
     * @param directory The directory where the Lucene index is stored.
     * @param codec Optional custom codec for the index; can be null to use Lucene's default codec.
     */
    private void indexDocs(Directory directory, Codec codec, List<Document> docs) throws IOException {
        // Initializes the default analyzer which breaks text into tokens and can apply additional processes like filtering.
        Analyzer defaultAnalyzer = new StandardAnalyzer();

        // Creates a set of stop words; set to case insensitive, so it considers "in, In, IN..." as the same.
        CharArraySet stopWords = new CharArraySet(Arrays.asList("in", "dei", "di"), true);
        Map<String, Analyzer> perFieldAnalyzers = new HashMap<>();

        // String "contenuto" has a standard analyzer that skips "stopWords"
        perFieldAnalyzers.put("contenuto", new StandardAnalyzer(stopWords));

        // "titolo" uses the white space tokenizer
        perFieldAnalyzers.put("titolo", new WhitespaceAnalyzer());

        // Wrapper that allows setting specific analyzers per field. If not set for a field, the default analyzer is used.
        Analyzer analyzer = new PerFieldAnalyzerWrapper(defaultAnalyzer, perFieldAnalyzers);

        // Initializes the configuration for the IndexWriter using the specified analyzer.
        IndexWriterConfig config = new IndexWriterConfig(analyzer);
        if (codec != null) {
            config.setCodec(codec);
        }
        // Initializes the IndexWriter with the given directory and configurations.
        IndexWriter writer = new IndexWriter(directory, config);
        writer.deleteAll();

        // Create a new Lucene document to be indexed.
        /*
        Document doc1 = new Document();
        doc1.add(new TextField("titolo", "Come diventare un ingegnere dei dati, Data Engineer?", Field.Store.YES));
        doc1.add(new TextField("contenuto", "Sembra che oggigiorno tutti vogliano diventare un Data Scientist  ...", Field.Store.YES));
        doc1.add(new StringField("data", "12 ottobre 2016", Field.Store.YES));

        Document doc2 = new Document();
        doc2.add(new TextField("titolo", "Curriculum Ingegneria dei Dati - Sezione di Informatica e Automazione", Field.Store.YES));
        doc2.add(new TextField("contenuto", "Curriculum. Ingegneria dei Dati. Laurea Magistrale in Ingegneria Informatica ...", Field.Store.YES)); */

        // Adds documents to the index; these additions are in-memory and not yet persisted.
        for (Document d: docs) {
            writer.addDocument(d);
        }

        // Adds documents to the index; these additions are in-memory and not yet persisted.
        //writer.addDocument(doc1);
        //writer.addDocument(doc2);

        // Documents become persistent
        writer.commit();

        // Closes the IndexWriter to free up resources.
        writer.close();
    }
}
