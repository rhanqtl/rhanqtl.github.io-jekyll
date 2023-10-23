public class Visitable {
  public static void main(String[] args) {
    Expr e = new UnaryExpr("-", new BinaryExpr("+", new Literal(2), new Literal(3)));
    System.out.println(e.accept(new EvalVisitor()));
  }
}

interface Expr {
  default double accept(Visitor v) {
    v.visit(this);
  }
}

class BinaryExpr implements Expr {
  Expr lhs;
  Expr rhs;
  String op;

  BinaryExpr(String op, Expr lhs, Expr rhs) {
    this.op = op;
    this.lhs = lhs;
    this.rhs = rhs;
  }
}

class UnaryExpr implements Expr {
  String op;
  Expr x;

  UnaryExpr(String op, Expr x) {
    this.op = op;
    this.x = x;
  }
}

class Literal implements Expr {
  double v;

  Literal(double v) {
    this.v = v;
  }
}

interface Visitor {
  double visit(BinaryExpr e);
  double visit(UnaryExpr e);
  double visit(Literal e);
}

class EvalVisitor implements Visitor {
  public double visit(BinaryExpr e) {
    switch (e.op) {
      case "+":
        return e.lhs.accept(this) + e.rhs.accept(this);
    }
  }
  public double visit(UnaryExpr e) {
    switch (e.op) {
      case "-":
        return -e.x.accept(this);
    }
  }
  public double visit(Literal e) {
    return e.v;
  }
}
