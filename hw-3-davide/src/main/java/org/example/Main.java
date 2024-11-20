package org.example;

import io.github.fededa.exceptions.EmptyUserInputException;
import io.github.fededa.inputhandler.InputHandler;
import io.github.fededa.lucenecustomhandler.LuceneCustomHandler;
import org.apache.lucene.analysis.core.WhitespaceAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.TopDocs;
import org.example.models.MyAbstractTable;
import org.example.models.RelevanceCriteria;

import java.util.*;

public class Main {
    public static void main(String[] args) {
        QueryParser parser = new QueryParser("titolo", new WhitespaceAnalyzer());
        // Builds query
        List<Document> docsList = new ArrayList<Document>();
        try {
            InputHandler ih = new InputHandler();
            String userInput = ih.readUserInput("What are you looking for today?\n");
            if(userInput.isEmpty()) throw new EmptyUserInputException();
            // Compie la ricerca e salva i documenti Lucene
            TopDocs queryDocumentsResult = new LuceneCustomHandler( new InputHandler()).runHw_3_davide(parser,docsList, userInput);
            // Istanzio la lista di tabelle che estrarrò dai documenti Lucene
            List<MyAbstractTable> tableExtractedFromQueryDocumentResult = new ArrayList<>();
            // Conversione da TopDocs (Lucene) a List<MyAbstractTable>
            // TODO: Implementare metodo per estrarre tabella da inserire in tableExtractedFromQueryDocumentResult
            // foreach Doc in queryDocumentsResult, extract table and put in tableExtractedFromQueryDocumentResult

            // queryResults    Map che associa ogni query alla lista delle tabelle recuperate (risultati della query).
            Map<String, List<MyAbstractTable>> queryResults = new HashMap<>();

            queryResults.put(userInput, tableExtractedFromQueryDocumentResult);

            // Metodo per riempire le gold tables
            Map<String, Set<MyAbstractTable>> relevantTablesMap = new HashMap<>();
            Set<MyAbstractTable> relevantTables = new HashSet<>();

            for (MyAbstractTable table : tableExtractedFromQueryDocumentResult) {
                if (RelevanceCriteria.isRelevant(userInput, table)) {
                    relevantTables.add(table);
                }
            }
            // Inserisce le tabelle trovate
            relevantTablesMap.put(userInput, relevantTables);

            double computedMRR = computeMRR(queryResults, relevantTablesMap);
            System.out.println("Current MMR is: " + computedMRR);

        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    public static double computeMRR(Map<String, List<MyAbstractTable>> queryResults,
                              Map<String, Set<MyAbstractTable>> relevantTables) {
        double sumReciprocalRanks = 0.0;
        int totalQueries = queryResults.size();

        for (String query : queryResults.keySet()) {
            List<MyAbstractTable> retrievedTables = queryResults.get(query);
            Set<MyAbstractTable> relevant = relevantTables.get(query);

            double reciprocalRank = 0.0;

            // Trova la posizione del primo risultato rilevante
            for (int i = 0; i < retrievedTables.size(); i++) {
                MyAbstractTable table = retrievedTables.get(i);
                if (relevant.contains(table)) {
                    reciprocalRank = 1.0 / (i + 1); // Posizione 1-based
                    break;
                }
            }

            sumReciprocalRanks += reciprocalRank;
        }

        return sumReciprocalRanks / totalQueries;
    }
}