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

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
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
    public TopDocs runHw_2(QueryParser parser, List<Document> docsList) throws Exception{
        Path luceneIndexPath = Paths.get("target/idx0");
        // Lucene's index is stored here
        try (Directory directory = FSDirectory.open(luceneIndexPath)) {

            // Opening the file-system directory for the Lucene index.
            indexExistingFiles(indexDocs(directory, new SimpleTextCodec(), docsList));
            // Opens a reader for the Lucene index; this is read-only and prevents modifications.
            try (IndexReader reader = DirectoryReader.open(directory)) {
                String userInput = ih.readUserInput("What are you looking for today?\n");
                if(userInput.isEmpty()) throw new EmptyUserInputException();
                //QueryParser parser = new QueryParser("titolo", new WhitespaceAnalyzer());
                // Builds query
                Query query = parser.parse(userInput);
                // Allows searching within Lucene's index
                IndexSearcher searcher = new IndexSearcher(reader);
                long startTime = System.currentTimeMillis();
                TopDocs results = searcher.search(query,10);
                System.out.println("Search time: " + (System.currentTimeMillis() - startTime) + "ms");
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
    private IndexWriter indexDocs(Directory directory, Codec codec, List<Document> docs) throws IOException {
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

        for (Document d: docs) {
            writer.addDocument(d);
        }

        // Documents become persistent
        writer.commit();

        return writer;
    }

    private void indexExistingFiles(IndexWriter writer) throws IOException {
        try {
            Path parentWorkingDir = Paths.get(System.getProperty("user.dir")).getParent();
            System.out.println("current working dir: " + parentWorkingDir.toString());
            String resourcePath = "IDD/hw-2/src/main/resources/documents";
            Path fullPath = parentWorkingDir.resolve("IDD/hw-2/src/main/resources/documents");
            if(parentWorkingDir.toString().contains("IDD")){
                fullPath = parentWorkingDir.resolve("hw-2/src/main/resources/documents");
            }

            System.out.println("full path: " + fullPath.toString());
            //Path fullPath = Paths.get("hw-2/src/main/resources/documents");
            File[] files = getFilesFromPath(fullPath);
            if (files != null) {
                for (File file : files) {
                    indexFile(writer, file);
                }
            } else {
                System.out.println("Directory not found or not accessible: " + fullPath);
            }
        } catch (Exception e) {
            System.out.println("Error accessing resource folder: " + e.toString());
            e.printStackTrace();
        } finally {
            commitAndCloseWriter(writer);
        }
    }

    private File[] getFilesFromPath(Path path) {
        File dir = new File(path.toUri());
        return dir.listFiles();
    }

    private void indexFile(IndexWriter writer, File file) throws IOException {
        Document document = new Document();
        document.add(new TextField("titolo", file.getName(), Field.Store.YES));

        String fileContent = readFileContent(file);
        if (fileContent != null) {
            document.add(new TextField("contenuto", fileContent, Field.Store.YES));
        }

        writer.addDocument(document);
    }

    private String readFileContent(File file) {
        StringBuilder content = new StringBuilder();

        try (BufferedReader reader = new BufferedReader(new FileReader(file))) {
            String line;
            while ((line = reader.readLine()) != null) {
                content.append(line).append(System.lineSeparator());
            }
        } catch (IOException e) {
            System.out.println("Error reading file content: " + file.getName() + ". Exception: " + e.toString());
            return null;
        }

        return content.toString();
    }

    private void commitAndCloseWriter(IndexWriter writer) throws IOException {
        writer.commit();
        writer.close();
    }


}













