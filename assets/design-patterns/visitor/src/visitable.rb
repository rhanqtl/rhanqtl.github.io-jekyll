#!/usr/bin/env ruby

class Expr
  def accept v
    method = "visit_" + self.class.name.split(/([A-Z][a-z]+)/).filter { |s| not s.empty? }.map { |s| s.downcase }.inject { |accum, p|
 accum + "_" + p }
    v.send method.to_sym, self
  end
end

class BinaryExpr < Expr
  attr_reader :op, :lhs, :rhs

  def initialize op, lhs, rhs
    @op = op
    @lhs = lhs
    @rhs = rhs
  end
end

class UnaryExpr < Expr
  attr_reader :op, :x

  def initialize op, x
    @op = op
    @x = x
  end
end

class Literal < Expr
  attr_reader :v

  def initialize v
    @v = v
  end
end

class EvalVisitor
  def visit_binary_expr e
    case e.op
    when "+"
      return e.lhs.accept(self) + e.rhs.accept(self)
    end
  end

  def visit_unary_expr e
    case e.op
    when "-"
      return -e.x.accept(self)
    end
  end

  def visit_literal e
    e.v
  end
end

p UnaryExpr.new(
  "-",
  BinaryExpr.new(
    "+",
    Literal.new(2),
    Literal.new(3),
  )
).accept(EvalVisitor.new)
