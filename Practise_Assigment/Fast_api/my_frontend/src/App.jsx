import { useEffect, useState } from "react"
import axios from "axios"

const API = "http://localhost:8000"

function App() {
  const [products, setProducts] = useState([])
  const [form, setForm] = useState({
    id: "",
    name: "",
    price: "",
    quantity: "",
    description: ""
  })

  // GET all products
  const fetchProducts = async () => {
    try {
      const res = await axios.get(`${API}/products`)
      setProducts(res.data)
    } catch (err) {
      console.error("Error fetching products:", err)
    }
  }

  // POST a new product
  const createProduct = async (product) => {
    try {
      const res = await axios.post(`${API}/products`, product)
      console.log("Product created:", res.data)
      fetchProducts()
    } catch (err) {
      console.error("Error creating product:", err.response?.data || err)
    }
  }

  // PUT update product
  const updateProduct = async (id, product) => {
    try {
      const res = await axios.put(`${API}/products?id=${id}`, product)
      console.log("Product updated:", res.data)
      fetchProducts()
    } catch (err) {
      console.error("Error updating product:", err.response?.data || err)
    }
  }

  // DELETE product
  const deleteProduct = async (id) => {
    try {
      const res = await axios.delete(`${API}/products?id=${id}`)
      console.log("Product deleted:", res.data)
      fetchProducts()
    } catch (err) {
      console.error("Error deleting product:", err.response?.data || err)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    const productData = {
      id: Number(form.id),
      name: form.name,
      price: Number(form.price),
      quantity: Number(form.quantity),
      description: form.description
    }

    const exists = products.some(p => p.id === form.id)

if (exists) {
  await updateProduct(form.id, productData)
} else {
  await createProduct(productData)
}
    setForm({ id: "", name: "", price: "", quantity: "", description: "" })
  }

  const editProduct = (product) => {
    setForm(product)
  }

  useEffect(() => {
    fetchProducts()
  }, [])

  return (
    <div className="min-h-screen bg-gray-100 p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Product Manager</h1>

      {/* FORM */}
      <form onSubmit={handleSubmit} className="bg-white p-4 rounded shadow mb-6 space-y-3">
        <input
          className="w-full border p-2 rounded"
          placeholder="Id"
          type="number"
          value={form.id ?? ""}
          onChange={e => setForm({ ...form, id: Number(e.target.value) })}
          required
        />
        <input
          className="w-full border p-2 rounded"
          placeholder="Name"
          value={form.name}
          onChange={e => setForm({ ...form, name: e.target.value })}
          required
        />
        <input
          className="w-full border p-2 rounded"
          placeholder="Price"
          type="number"
          value={form.price}
          onChange={e => setForm({ ...form, price: e.target.value })}
          required
        />
        <input
          className="w-full border p-2 rounded"
          placeholder="Quantity"
          type="number"
          value={form.quantity}
          onChange={e => setForm({ ...form, quantity: e.target.value })}
          required
        />
        <textarea
          className="w-full border p-2 rounded"
          placeholder="Description"
          value={form.description}
          onChange={e => setForm({ ...form, description: e.target.value })}
        />
        <button className="bg-blue-600 text-white px-4 py-2 rounded">
          Add Product
        </button>
      </form>

      {/* LIST */}
      <div className="grid gap-4">
        {products.map(product => (
          <div key={product.id} className="bg-white p-4 rounded shadow">
            <h1 className="text-red-800">{product.id}</h1>
            <h2 className="font-semibold">{product.name}</h2>
            <p className="text-sm text-gray-600">{product.description}</p>
            <p className="text-sm">₹{product.price} | Qty: {product.quantity}</p>

            <div className="mt-3 flex gap-2">
              <button
                className="px-3 py-1 bg-yellow-500 text-white rounded"
                onClick={() => editProduct(product)}
              >
                Edit
              </button>
              <button
                className="px-3 py-1 bg-red-600 text-white rounded"
                onClick={() => deleteProduct(product.id)}
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default App
