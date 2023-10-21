package io.github.fededa.lucenecustomhandler;

import org.apache.lucene.document.Document;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.TopDocs;

import java.util.List;

/**
 * Interface that defines interactions with Lucene
 *
 * @author Federico D'Armini
 * @version 1.0
 * @since 2023-10-20
 */

public interface LuceneCustomHandlerInterface {

    /**
     *  Runs 2nd Homework's assignments
     */
    TopDocs runHw_2(QueryParser parser, List<Document> documentsList) throws Exception;
}
