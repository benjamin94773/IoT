db = db.getSiblingDB('tienda');

db.products.insertMany([
  { name: 'Laptop', price: 3500000, stock: 5 },
  { name: 'Mouse', price: 80000, stock: 20 },
  { name: 'Keyboard', price: 150000, stock: 12 }
]);

db.customers.insertMany([
  { name: 'Ana', email: 'ana@example.com' },
  { name: 'Luis', email: 'luis@example.com' }
]);

db.orders.insertOne({
  customerId: 1,
  date: ISODate("2026-08-24T00:00:00Z"),
  items: [
    { product: "Laptop", quantity: 1 },
    { product: "Mouse", quantity: 2 }
  ]
})