import model.*;
import service.*;

import java.util.Scanner;

public class Main {

    static int accountCounter = 1001;

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        AuthService authService = new AuthService();
        BankService bankService = new BankService();

        Account currentUser = null;

        while (true) {
            System.out.println("\n--- Banking System ---");
            System.out.println("1. Create Account");
            System.out.println("2. Login");
            System.out.println("3. Exit");

            int choice = sc.nextInt();

            switch (choice) {
                case 1:
                    sc.nextLine();
                    System.out.print("Enter username: ");
                    String username = sc.nextLine();

                    System.out.print("Enter password: ");
                    String password = sc.nextLine();

                    System.out.print("Initial balance: ");
                    double balance = sc.nextDouble();

                    System.out.println("1. Savings  2. Current");
                    int type = sc.nextInt();

                    Account acc;
                    if (type == 1) {
                        acc = new SavingsAccount(accountCounter++, username, password, balance);
                    } else {
                        acc = new CurrentAccount(accountCounter++, username, password, balance);
                    }

                    authService.register(acc);
                    System.out.println("Account created successfully!");
                    break;

                case 2:
                    sc.nextLine();
                    System.out.print("Username: ");
                    String u = sc.nextLine();

                    System.out.print("Password: ");
                    String p = sc.nextLine();

                    currentUser = authService.login(u, p);

                    if (currentUser == null) {
                        System.out.println("Invalid credentials!");
                        break;
                    }

                    System.out.println("Login successful!");

                    while (true) {
                        System.out.println(
                                "\n1. Deposit\n2. Withdraw\n3. Transfer\n4. Balance\n5. Transactions\n6. Logout");
                        int op = sc.nextInt();

                        if (op == 6)
                            break;

                        switch (op) {
                            case 1:
                                System.out.print("Amount: ");
                                currentUser.deposit(sc.nextDouble());
                                break;

                            case 2:
                                System.out.print("Amount: ");
                                if (!currentUser.withdraw(sc.nextDouble())) {
                                    System.out.println("Insufficient balance!");
                                }
                                break;

                            case 3:
                                sc.nextLine();
                                System.out.print("Transfer to username: ");
                                String toUser = sc.nextLine();

                                Account receiver = authService.getAccount(toUser);
                                if (receiver == null) {
                                    System.out.println("User not found!");
                                    break;
                                }

                                System.out.print("Amount: ");
                                double amt = sc.nextDouble();

                                bankService.transfer(currentUser, receiver, amt);
                                break;

                            case 4:
                                System.out.println("Balance: " + currentUser.getBalance());
                                break;

                            case 5:
                                currentUser.showTransactions();
                                break;
                        }
                    }
                    break;

                case 3:
                    System.out.println("Thank you!");
                    return;
            }
        }
    }
}