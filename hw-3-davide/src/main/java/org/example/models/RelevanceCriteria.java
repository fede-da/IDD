package org.example.models;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

public class RelevanceCriteria {

    /**
     * Determina se una tabella è rilevante per una query basandosi su criteri predefiniti.
     *
     * @param query La query per cui si valuta la rilevanza.
     * @param table La tabella da valutare.
     * @return True se la tabella è rilevante, false altrimenti.
     */
    public static boolean isRelevant(String query, MyAbstractTable table) {
        // Semplice criterio: la tabella è rilevante se contiene tutte le parole chiave della query nel nome
        Set<String> queryKeywords = new HashSet<>(Arrays.asList(query.toLowerCase().split("\\s+")));
        Set<String> tableKeywords = new HashSet<>(Arrays.asList(table.getTableName().toLowerCase().split("_")));

        return tableKeywords.containsAll(queryKeywords);
    }
}
