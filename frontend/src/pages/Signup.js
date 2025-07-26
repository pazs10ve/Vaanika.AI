import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { ToastContainer } from 'react-toastify'
import { handleError, handleSuccess } from '../utils'
import bgImage from "../assets/background.png";

function Signup() {
    const [signupInfo, setSignupInfo] = useState({
        name: '',
        email: '',
        password: ''
    })

    const navigate = useNavigate()

    const handleChange = (e) => {
        const { name, value } = e.target
        setSignupInfo(prev => ({ ...prev, [name]: value }))
    }

    const handleSignup = async (e) => {
        e.preventDefault()
        const { name, email, password } = signupInfo
        if (!name || !email || !password) {
            return handleError('Name, email and password are required')
        }
        try {
            const url = `http://localhost:4000/auth/signup`
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(signupInfo)
            })
            const result = await response.json()
            const { success, message, error } = result
            if (success) {
                handleSuccess(message)
                setTimeout(() => navigate('/login'), 1000)
            } else {
                handleError(error?.details[0]?.message || message)
            }
        } catch (err) {
            handleError(err.message)
        }
    }

    return (
        <div className="min-h-screen flex flex-col md:flex-row">
            {/* Left: Signup Form */}
            <div className="w-full md:w-1/2 flex items-center justify-center bg-black px-8 py-12">
                <div className="w-full max-w-md space-y-6">
                    <h1 className="text-4xl font-bold text-white mb-4 tracking-tight">Join <span className="text-green-400">KalaaSetu</span></h1>
                    <p className="text-zinc-400 mb-6">Create your free account</p>

                    <form onSubmit={handleSignup} className="space-y-5">
                        <div>
                            <label htmlFor='name' className="block mb-2 text-sm text-zinc-300">Name</label>
                            <input
                                type='text'
                                name='name'
                                autoFocus
                                placeholder='Your full name'
                                value={signupInfo.name}
                                onChange={handleChange}
                                className="w-full px-4 py-3 bg-zinc-900 border border-zinc-700 rounded-xl text-white placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-green-500"
                            />
                        </div>

                        <div>
                            <label htmlFor='email' className="block mb-2 text-sm text-zinc-300">Email</label>
                            <input
                                type='email'
                                name='email'
                                placeholder='you@example.com'
                                value={signupInfo.email}
                                onChange={handleChange}
                                className="w-full px-4 py-3 bg-zinc-900 border border-zinc-700 rounded-xl text-white placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-green-500"
                            />
                        </div>

                        <div>
                            <label htmlFor='password' className="block mb-2 text-sm text-zinc-300">Password</label>
                            <input
                                type='password'
                                name='password'
                                placeholder='••••••••'
                                value={signupInfo.password}
                                onChange={handleChange}
                                className="w-full px-4 py-3 bg-zinc-900 border border-zinc-700 rounded-xl text-white placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-green-500"
                            />
                        </div>

                        <button
                            type='submit'
                            className="w-full py-3 bg-green-500 hover:bg-green-600 transition rounded-xl font-semibold text-black"
                        >
                            Sign Up
                        </button>
                    </form>

                    <p className="text-sm text-zinc-500 mt-4">
                        Already have an account?
                        <Link to="/login" className="text-green-400 hover:underline ml-1">Login</Link>
                    </p>
                </div>
            </div>

            {/* Right: Visual Side */}
            <div
                    className="hidden md:block w-full md:w-1/2 bg-cover bg-center relative"
                    style={{ backgroundImage: `url(${bgImage})` }}
                  >
                    <div className="absolute inset-0 flex items-center justify-center">
                      <div className="text-center px-6">
                        <h2 className="text-5xl font-extrabold text-white drop-shadow-lg">
                          KalaaSetu
                        </h2>
                        <p className="mt-4 text-zinc-300 text-lg max-w-md mx-auto">
                          A bridge to intelligent multimedia — from text to video, graphics, and voice.
                        </p>
                      </div>
                    </div>
                  </div>

            <ToastContainer />
        </div>
    )
}

export default Signup
