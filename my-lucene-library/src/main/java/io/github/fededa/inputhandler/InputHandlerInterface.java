package io.github.fededa.inputhandler;

import com.fasterxml.jackson.databind.JsonNode;

public interface InputHandlerInterface {
    String readUserInput(String messageToDisplay);

    JsonNode readJsonFile(String pathToJsonFile);
}
