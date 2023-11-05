package io.github.fededa;

import io.github.fededa.inputhandler.InputHandler;
import io.github.fededa.lucenecustomhandler.LuceneCustomHandler;

import java.io.IOException;
import java.text.ParseException;

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args )
    {
        new LuceneCustomHandler( new InputHandler()).runHw_3("setExample.json");
    }
}
