#include <iostream>

using Time = int64_t;

class DateTimeFormatter {
 public:
  virtual std::string format(const Time &t) = 0;
  virtual ~DateTimeFormatter() {}
};

class StandardDateTimeFormatter : public DateTimeFormatter {
 public:
  std::string format(const Time &t) override {
    return "2006-01-02 15:04:05.006";
  }
  virtual ~StandardDateTimeFormatter() {}
};

class AmericanDateTimeFormatter : public DateTimeFormatter {
 public:
  std::string format(const Time &t) override {
    return "Jan. 02, 2006 - 15:04:05";
  }
  virtual ~AmericanDateTimeFormatter() {}
};

void foo(const DateTimeFormatter &f) { std::cout << "abstract" << std::endl; }

void foo(const StandardDateTimeFormatter &f) {
  std::cout << "standard" << std::endl;
}

void foo(const AmericanDateTimeFormatter &f) {
  std::cout << "american" << std::endl;
}

int main() {
  std::cout << "name of formatter: ";
  std::string name;
  std::cin >> name;
  DateTimeFormatter *f;
  if (name == "standard") {
    f = new StandardDateTimeFormatter{};
  } else if (name == "american") {
    f = new AmericanDateTimeFormatter{};
  }
  // foo(*f);
  std::cout << f->format(0) << std::endl;

  delete f;
}
