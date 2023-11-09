package io.github.fededa.exceptions;

public class EmptyUserInputException extends RuntimeException{
    @Override
    public String toString() {
        return super.toString() + "User Input is empty";
    }
}
