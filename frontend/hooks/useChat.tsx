"use client"

import { Message } from '@/lib/type'
import { useCallback, useState } from 'react'

const useChat = () => {
    const [input, setInput] = useState<string>('')
    const [loading, setLoading] = useState<boolean>(false)
    const [messages, setMesages] = useState<Message[]>([])


    const handleSubmit = useCallback(() => {
        setLoading(true)
        // make request to some ai
        // or give option to selecting pdf then ask question if then also need to give chat id          
        
          setTimeout(() => {
            setMesages([
                {
                  id: "2",
                  created_at: "2024-02-18T10:01:00Z",
                  message: "Hey! I need some help with TypeScript.",
                  type: "user",
                },
                {
                  id: "3",
                  created_at: "2024-02-18T10:02:00Z",
                  message: "Sure! What do you need help with?",
                  type: "bot",
                },
                {
                  id: "4",
                  created_at: "2024-02-18T10:03:00Z",
                  message: "How do I define a type for an object?",
                  type: "user",
                },
                {
                  id: "5",
                  created_at: "2024-02-18T10:04:00Z",
                  message: "You can use the `type` keyword. For example: `type User = { name: string; age: number; }`",
                  type: "bot",
                },
                {
                  id: "6",
                  created_at: "2024-02-18T10:05:00Z",
                  message: "Got it! Thanks.",
                  type: "user",
                },
                {
                  id: "7",
                  created_at: "2024-02-18T10:06:00Z",
                  message: "You're welcome! 😊",
                  type: "bot",
                },
                {
                    id: "2",
                    created_at: "2024-02-18T10:01:00Z",
                    message: "Hey! I need some help with TypeScript.",
                    type: "user",
                  },
                  {
                    id: "3",
                    created_at: "2024-02-18T10:02:00Z",
                    message: "Sure! What do you need help with?",
                    type: "bot",
                  },
                  {
                    id: "4",
                    created_at: "2024-02-18T10:03:00Z",
                    message: "How do I define a type for an object?",
                    type: "user",
                  },
                  {
                    id: "5",
                    created_at: "2024-02-18T10:04:00Z",
                    message: "You can use the `type` keyword. For example: `type User = { name: string; age: number; }`",
                    type: "bot",
                  },
                  {
                    id: "6",
                    created_at: "2024-02-18T10:05:00Z",
                    message: "Got it! Thanks.",
                    type: "user",
                  },
                  {
                    id: "7",
                    created_at: "2024-02-18T10:06:00Z",
                    message: "You're welcome! 😊",
                    type: "bot",
                  },{
                    id: "2",
                    created_at: "2024-02-18T10:01:00Z",
                    message: "Hey! I need some help with TypeScript.",
                    type: "user",
                  },
                  {
                    id: "3",
                    created_at: "2024-02-18T10:02:00Z",
                    message: "Sure! What do you need help with?",
                    type: "bot",
                  },
                  {
                    id: "4",
                    created_at: "2024-02-18T10:03:00Z",
                    message: "How do I define a type for an object?",
                    type: "user",
                  },
                  {
                    id: "5",
                    created_at: "2024-02-18T10:04:00Z",
                    message: "You can use the `type` keyword. For example: `type User = { name: string; age: number; }`",
                    type: "bot",
                  },
                  {
                    id: "6",
                    created_at: "2024-02-18T10:05:00Z",
                    message: "Got it! Thanks.",
                    type: "user",
                  },
                  {
                    id: "7",
                    created_at: "2024-02-18T10:06:00Z",
                    message: "You're welcome! 😊",
                    type: "bot",
                  },{
                    id: "2",
                    created_at: "2024-02-18T10:01:00Z",
                    message: "Hey! I need some help with TypeScript.",
                    type: "user",
                  },
                  {
                    id: "3",
                    created_at: "2024-02-18T10:02:00Z",
                    message: "Sure! What do you need help with?",
                    type: "bot",
                  },
                  {
                    id: "4",
                    created_at: "2024-02-18T10:03:00Z",
                    message: "How do I define a type for an object?",
                    type: "user",
                  },
                  {
                    id: "5",
                    created_at: "2024-02-18T10:04:00Z",
                    message: "You can use the `type` keyword. For example: `type User = { name: string; age: number; }`",
                    type: "bot",
                  },
                  {
                    id: "6",
                    created_at: "2024-02-18T10:05:00Z",
                    message: "Got it! Thanks.",
                    type: "user",
                  },
                  {
                    id: "7",
                    created_at: "2024-02-18T10:06:00Z",
                    message: "You're welcome! 😊",
                    type: "bot",
                  },   
              ])
              setLoading(false)
          },10000
          )
          
    },[])

    return {input, setInput, messages, handleSubmit, loading}
}

export default useChat
