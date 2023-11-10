package io.fededa.idd;

import io.github.fededa.inputhandler.InputHandler;
import io.github.fededa.lucenecustomhandler.LuceneCustomHandler;

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args )
    {
        System.out.println( new LuceneCustomHandler( new InputHandler()).runHw_3("/Users/kaguyasama/Downloads/tables.json",5).toString());
    }
}
