package com.idd.app;

import io.github.fededa.exceptions.EmptyUserInputException;
import io.github.fededa.inputhandler.InputHandlerInterface;
import io.github.fededa.lucenecustomhandler.LuceneCustomHandler;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.CharArraySet;
import org.apache.lucene.analysis.core.WhitespaceAnalyzer;
import org.apache.lucene.analysis.miscellaneous.PerFieldAnalyzerWrapper;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.Assertions;

import java.util.*;

import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

/**
 * Unit test for Lucene queries.
 */
public class Hw2Test {
    // Arrange
    List<Document> docsList = new ArrayList<>();
    InputHandlerInterface mockInputHandler = mock(InputHandlerInterface.class);
    LuceneCustomHandler lch = new LuceneCustomHandler(mockInputHandler);
    CharArraySet stopWords = new CharArraySet(Arrays.asList("in", "dei", "di"), true);
    Map<String, Analyzer> perFieldAnalyzers = new HashMap<>();
    Document doc1 = new Document();
    Document doc2 = new Document();

    @BeforeEach
    public void setup() {

        doc1.add(new TextField("titolo", "Come diventare un ingegnere dei dati, Data Engineer?", Field.Store.YES));
        doc1.add(new TextField("contenuto", "Sembra che oggigiorno tutti vogliano diventare un Data Scientist ...", Field.Store.YES));
        doc1.add(new StringField("data", "12 ottobre 2016", Field.Store.YES));

        doc2.add(new TextField("titolo", "Curriculum Ingegneria dei Dati - Sezione di Informatica e Automazione", Field.Store.YES));
        doc2.add(new TextField("contenuto", "Curriculum. Ingegneria dei Dati. Laurea Magistrale in Ingegneria Informatica ...", Field.Store.YES));

        docsList.addAll(Arrays.asList(doc1, doc2));
    }
    @Test
    public void onEmptyUserInputThenEmptyUserInputExceptionIsThrown() {
        when(mockInputHandler.readUserInput(anyString())).thenReturn("");
        QueryParser qp = mock (QueryParser.class);
        Assertions.assertThrows(EmptyUserInputException.class, () -> lch.runHw_2(qp, docsList));
    }

    @Test
    public void whenSearchingForRandomWordsInOneTitoloThenNoDocumentIsRetrieved() throws Exception {
        when(mockInputHandler.readUserInput(anyString())).thenReturn("dfhsjgdhfgahjdflgedlhyrg ioioioiioiioioioioooiii bcxnzvbnv");
        QueryParser qp = new QueryParser("titolo", new WhitespaceAnalyzer());
        int len = lch.runHw_2(qp, docsList).scoreDocs.length;
        Assertions.assertTrue(len==0);
    }

    @Test
    public void whenSearchingForWordsMatchInTitoloThenNoDocumentIsRetrieved() throws Exception {
        when(mockInputHandler.readUserInput(anyString())).thenReturn("come engineer");
        QueryParser qp = new QueryParser("titolo", new WhitespaceAnalyzer());
        int len = lch.runHw_2(qp, docsList).scoreDocs.length;
        Assertions.assertTrue(len==0);
    }

    @Test
    public void whenSearchingForExactWordsMatchInTitoloThenOneDocumentIsRetrieved() throws Exception {
        when(mockInputHandler.readUserInput(anyString())).thenReturn("Come engineer");
        QueryParser qp = new QueryParser("titolo", new WhitespaceAnalyzer());
        int len = lch.runHw_2(qp, docsList).scoreDocs.length;
        Assertions.assertTrue(len==1);
    }

    @Test
    public void whenSearchingForWordMatchesInTwoOrMoreTitoloThenAtLeastTwoDocumentsAreRetrieved() throws Exception {
        when(mockInputHandler.readUserInput(anyString())).thenReturn("Come Engineer Sezione Informatica");
        QueryParser qp = new QueryParser("titolo", new WhitespaceAnalyzer());
        int len = lch.runHw_2(qp, docsList).scoreDocs.length;
        Assertions.assertTrue(len>1);
    }

    @Test
    public void whenSearchingForRandomWordsInContenutoNoDocumetIsRetrieved() throws Exception {
        when(mockInputHandler.readUserInput(anyString())).thenReturn("dfhsjgdhfgahjdflgedlhyrg ioioioiioiioioioioooiii bcxnzvbnv");
        QueryParser qp = new QueryParser("contenuto", new StandardAnalyzer());
        int len = lch.runHw_2(qp, docsList).scoreDocs.length;
        Assertions.assertTrue(len==0);
    }

    @Test
    public void ifQueryAboutContenutoFieldContainsOnlyStopWordsThenNoDocumentIsRetrieved() throws Exception {
        when(mockInputHandler.readUserInput(anyString())).thenReturn("dei in di ");
        perFieldAnalyzers.put("contenuto", new StandardAnalyzer(stopWords));
        Analyzer analyzer = new PerFieldAnalyzerWrapper(new StandardAnalyzer(), perFieldAnalyzers);
        QueryParser qp = new QueryParser("contenuto", new StandardAnalyzer(stopWords));
        Assertions.assertEquals(0,lch.runHw_2(qp, docsList).scoreDocs.length);
    }

    @Test
    public void onQueryAboutContentFieldNotInStopWordsThenAtLeastOneDocumentIsRetrieved() throws Exception {
        when(mockInputHandler.readUserInput(anyString())).thenReturn("un\n");
        perFieldAnalyzers.put("contenuto", new StandardAnalyzer(stopWords));
        Analyzer analyzer = new PerFieldAnalyzerWrapper(new StandardAnalyzer(), perFieldAnalyzers);
        QueryParser qp = new QueryParser("contenuto", new StandardAnalyzer(stopWords));
        int len = lch.runHw_2(qp, docsList).scoreDocs.length;
        Assertions.assertTrue(len>0);
    }

    @Test
    public void whenSearchingForExactWordsMatchInContenutoThenOneDocumentIsRetrieved() throws Exception {
        when(mockInputHandler.readUserInput(anyString())).thenReturn("Sembra che tutti");
        QueryParser qp = new QueryParser("contenuto", new StandardAnalyzer());
        int len = lch.runHw_2(qp, docsList).scoreDocs.length;
        Assertions.assertTrue(len==1);
    }
    @Test
    public void whenSearchingForWordMatchesInTwoOrMoreContenutoThenAtLeastTwoDocumentsAreRetrieved() throws Exception {
        when(mockInputHandler.readUserInput(anyString())).thenReturn("Sembra che tutti Ingegneria dei dati");
        QueryParser qp = new QueryParser("titolo", new WhitespaceAnalyzer());
        int len = lch.runHw_2(qp, docsList).scoreDocs.length;
        Assertions.assertTrue(len>1);
    }

    @Test
    public void sameWordsButDifferentPunctuationProducesNoResults() throws Exception {
        when(mockInputHandler.readUserInput(anyString())).thenReturn("Sembra. che. tutti. Ingegneria. dei. dati.");
        QueryParser qp = new QueryParser("titolo", new WhitespaceAnalyzer());
        int len = lch.runHw_2(qp, docsList).scoreDocs.length;
        Assertions.assertTrue(len==0);
    }

}




























