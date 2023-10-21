package io.github.fededa.inputhandler;

import org.apache.lucene.queryparser.classic.QueryParser;

import java.util.Scanner;

public class InputHandler implements InputHandlerInterface {

    /**
     *  Reads user input
     */
    @Override
    public String readUserInput(String messageToDisplay) {
        Scanner scanner = new Scanner(System.in);
        System.out.print(messageToDisplay);
        String userInput = scanner.nextLine();
        scanner.close();
        // Escapes Lucene's special characters
        return QueryParser.escape(userInput);
    }
}
