package service;

import model.Account;
import model.Transaction;

public class BankService {

    public void transfer(Account from, Account to, double amount) {
        if (from.withdraw(amount)) {
            to.deposit(amount);

            from.addTransaction(new Transaction("TRANSFER TO " + to.getUsername(), amount));
            to.addTransaction(new Transaction("RECEIVED FROM " + from.getUsername(), amount));

            System.out.println("Transfer successful!");
        } else {
            System.out.println("Insufficient balance!");
        }
    }
}