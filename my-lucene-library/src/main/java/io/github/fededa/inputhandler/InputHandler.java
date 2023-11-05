package io.github.fededa.inputhandler;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.lucene.queryparser.classic.QueryParser;

import java.io.File;
import java.io.IOException;
import java.net.URISyntaxException;
import java.net.URL;
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
    @Override
    public JsonNode readJsonFile(String pathToJsonFile) {
        ObjectMapper mapper = new ObjectMapper();
        JsonNode rootNode = null;
        try{
            URL filePath = getClass().getClassLoader().getResource(pathToJsonFile);
            if (filePath==null){
                throw new IOException("Resource not found, filepath for jsonTables file is null");
            }
            rootNode = mapper.readTree(new File(filePath.toURI()));
            // Print the map to see the content
            //System.out.println(rootNode);
        } catch (IOException e) {
            e.printStackTrace();
        } catch (URISyntaxException e) {
            e.printStackTrace();
        }
        return rootNode;
    }
}
