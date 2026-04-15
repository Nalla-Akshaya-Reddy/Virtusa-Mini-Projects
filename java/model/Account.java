package model;

import java.util.ArrayList;

public abstract class Account {
    protected int accountId;
    protected String username;
    protected String password;
    protected double balance;
    protected ArrayList<Transaction> transactions;

    public Account(int accountId, String username, String password, double balance) {
        this.accountId = accountId;
        this.username = username;
        this.password = password;
        this.balance = balance;
        this.transactions = new ArrayList<>();
    }

    public int getAccountId() {
        return accountId;
    }

    public String getUsername() {
        return username;
    }

    public boolean checkPassword(String password) {
        return this.password.equals(password);
    }

    public double getBalance() {
        return balance;
    }

    public void deposit(double amount) {
        balance += amount;
        transactions.add(new Transaction("DEPOSIT", amount));
    }

    public boolean withdraw(double amount) {
        if (balance >= amount) {
            balance -= amount;
            transactions.add(new Transaction("WITHDRAW", amount));
            return true;
        }
        return false;
    }

    public void addTransaction(Transaction t) {
        transactions.add(t);
    }

    public void showTransactions() {
        for (Transaction t : transactions) {
            System.out.println(t);
        }
    }

    public abstract String getAccountType();
}