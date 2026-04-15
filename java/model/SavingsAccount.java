package model;

public class SavingsAccount extends Account {

    public SavingsAccount(int accountId, String username, String password, double balance) {
        super(accountId, username, password, balance);
    }

    @Override
    public String getAccountType() {
        return "Savings Account";
    }
}