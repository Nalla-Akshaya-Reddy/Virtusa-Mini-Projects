package service;

import model.Account;
import java.util.HashMap;

public class AuthService {
    private HashMap<String, Account> users = new HashMap<>();

    public void register(Account account) {
        users.put(account.getUsername(), account);
    }

    public Account login(String username, String password) {
        Account acc = users.get(username);
        if (acc != null && acc.checkPassword(password)) {
            return acc;
        }
        return null;
    }

    public Account getAccount(String username) {
        return users.get(username);
    }
}