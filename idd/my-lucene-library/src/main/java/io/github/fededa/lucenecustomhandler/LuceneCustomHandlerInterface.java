package io.github.fededa.lucenecustomhandler;

import org.apache.lucene.search.TopDocs;

/**
 * Interface that defines interactions with Lucene
 *
 * @author Federico D'Armini
 * @version 1.0
 * @since 2023-10-20
 */

public interface LuceneCustomHandlerInterface {

    void printHelloWorldtTest();

    /**
     *  Runs 2nd Homework's assignments
     */

    TopDocs runHw_2() throws Exception;
}
