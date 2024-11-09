import java.util.*;

class Vehicle {
    private String vehicleId;
    private String type;
    private boolean isAvailable;
    private double rentalRate;

    public Vehicle(String vehicleId, String type, double rentalRate) {
        this.vehicleId = vehicleId;
        this.type = type;
        this.isAvailable = true;
        this.rentalRate = rentalRate;
    }

    public String getVehicleId() { return vehicleId; }
    public String getType() { return type; }
    public boolean isAvailable() { return isAvailable; }
    public double getRentalRate() { return rentalRate; }
    public void setAvailable(boolean available) { isAvailable = available; }
}

class Customer {
    private String customerId;
    private String name;
    private String contactInfo;

    public Customer(String customerId, String name, String contactInfo) {
        this.customerId = customerId;
        this.name = name;
        this.contactInfo = contactInfo;
    }

    public String getCustomerId() { return customerId; }
    public String getName() { return name; }
    public String getContactInfo() { return contactInfo; }
}

class Rental {
    private String rentalId;
    private Vehicle vehicle;
    private Customer customer;
    private Date startDate;
    private Date endDate;
    private double totalCost;

    public Rental(String rentalId, Vehicle vehicle, Customer customer, Date startDate, Date endDate) {
        this.rentalId = rentalId;
        this.vehicle = vehicle;
        this.customer = customer;
        this.startDate = startDate;
        this.endDate = endDate;
        calculateTotalCost();
    }

    private void calculateTotalCost() {
        long diffInMillies = endDate.getTime() - startDate.getTime();
        long diffInDays = diffInMillies / (24 * 60 * 60 * 1000);
        this.totalCost = diffInDays * vehicle.getRentalRate();
    }

    public double getTotalCost() { return totalCost; }
    public Vehicle getVehicle() { return vehicle; }
    public String getRentalId() { return rentalId; }
}

class RentalSystem {
    private List<Vehicle> vehicles;
    private List<Customer> customers;
    private List<Rental> rentals;

    public RentalSystem() {
        vehicles = new ArrayList<>();
        customers = new ArrayList<>();
        rentals = new ArrayList<>();
    }

    public void addVehicle(Vehicle vehicle) {
        vehicles.add(vehicle);
    }

    public void addCustomer(Customer customer) {
        customers.add(customer);
    }

    public Rental rentVehicle(String vehicleId, String customerId, Date startDate, Date endDate) {
        Vehicle vehicle = findVehicle(vehicleId);
        Customer customer = findCustomer(customerId);

        if (vehicle == null || customer == null) {
            return null;
        }

        if (!vehicle.isAvailable()) {
            System.out.println("Vehicle is not available");
            return null;
        }

        String rentalId = "R" + (rentals.size() + 1);
        Rental rental = new Rental(rentalId, vehicle, customer, startDate, endDate);
        vehicle.setAvailable(false);
        rentals.add(rental);
        return rental;
    }

    public void returnVehicle(String rentalId) {
        Rental rental = findRental(rentalId);
        if (rental != null) {
            rental.getVehicle().setAvailable(true);
            System.out.println("Total cost: $" + rental.getTotalCost());
        }
    }

    private Vehicle findVehicle(String vehicleId) {
        return vehicles.stream()
                .filter(v -> v.getVehicleId().equals(vehicleId))
                .findFirst()
                .orElse(null);
    }

    private Customer findCustomer(String customerId) {
        return customers.stream()
                .filter(c -> c.getCustomerId().equals(customerId))
                .findFirst()
                .orElse(null);
    }

    private Rental findRental(String rentalId) {
        return rentals.stream()
                .filter(r -> r.getRentalId().equals(rentalId))
                .findFirst()
                .orElse(null);
    }
}

public class Main {
    public static void main(String[] args) {
        RentalSystem rentalSystem = new RentalSystem();

        // Add vehicles
        rentalSystem.addVehicle(new Vehicle("V1", "Car", 50.0));
        rentalSystem.addVehicle(new Vehicle("V2", "Motorcycle", 30.0));

        // Add customers
        rentalSystem.addCustomer(new Customer("C1", "John Doe", "john@email.com"));
        rentalSystem.addCustomer(new Customer("C2", "Jane Smith", "jane@email.com"));

        // Rent a vehicle
        Date startDate = new Date();
        Calendar c = Calendar.getInstance();
        c.setTime(startDate);
        c.add(Calendar.DATE, 3);  // Rent for 3 days
        Date endDate = c.getTime();

        Rental rental = rentalSystem.rentVehicle("V1", "C1", startDate, endDate);
        if (rental != null) {
            System.out.println("Vehicle rented successfully");
            System.out.println("Total cost: $" + rental.getTotalCost());
        }

        // Return vehicle
        rentalSystem.returnVehicle("R1");
    }
}
