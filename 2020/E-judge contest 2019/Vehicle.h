class Car : public Vehicle{
public:
    virtual bool canDrive() const override {
        return true;
    }

    virtual bool canSail() const override {
        return false;
    }

    virtual bool canFly() const override {
        return false;
    }

    virtual ~Car() {};
 };

class Ship : public Vehicle {
public:
    bool canDrive() const override final {
        return false;
    }

    bool canSail() const override final {
        return true;
    }

    bool canFly() const override final {
        return false;
    }

    ~Ship() {};
};

class Plane : public Vehicle {
public:
    bool canDrive() const override final {
        return false;
    }

    bool canSail() const override final {
        return false;
    }

    bool canFly() const override final {
        return true;
    }

    ~Plane() {};
};

class Truck : public Car {
public:
    bool canDrive() const override final {
        return true;
    }

    bool canSail() const override final {
        return false;
    }

    bool canFly() const override final {
        return false;
    }
};