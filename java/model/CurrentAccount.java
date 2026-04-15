package model;

public class CurrentAccount extends Account {

    public CurrentAccount(int accountId, String username, String password, double balance) {
        super(accountId, username, password, balance);
    }

    @Override
    public String getAccountType() {
        return "Current Account";
    }
}