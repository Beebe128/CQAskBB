"use client"

import { useEffect, useMemo, useRef } from "react"
import type { Hd2dPayload } from "../api/hd2d"

export interface Hd2dViewerProps {
  payload?: Hd2dPayload
  hiddenLayers?: string[]
}

const COLORS: Record<string, string> = {
  bg_far: "#7ba7ff",
  bg_mid: "#4f7de0",
  bg_near: "#3456ad",
  sprites: "#ffcc5a",
  effects: "#dd7dff",
  ui: "#ffffff",
}

export default function Hd2dViewer({ payload, hiddenLayers = [] }: Hd2dViewerProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null)

  const visibleQuads = useMemo(() => {
    if (!payload) {
      return []
    }

    const hiddenSet = new Set(hiddenLayers)
    return payload.quads
      .filter((quad) => !hiddenSet.has(quad.layer))
      .slice()
      .sort((a, b) => {
        const az = a.world.reduce((sum, point) => sum + point[2], 0) / a.world.length
        const bz = b.world.reduce((sum, point) => sum + point[2], 0) / b.world.length
        return az - bz
      })
  }, [payload, hiddenLayers])

  const bounds = useMemo(() => {
    if (!payload || visibleQuads.length === 0) {
      return null
    }

    let minX = Infinity
    let minY = Infinity
    let maxX = -Infinity
    let maxY = -Infinity

    for (const quad of visibleQuads) {
      for (const [x, y] of quad.screen) {
        minX = Math.min(minX, x)
        minY = Math.min(minY, y)
        maxX = Math.max(maxX, x)
        maxY = Math.max(maxY, y)
      }
    }

    return { minX, minY, maxX, maxY }
  }, [payload, visibleQuads])

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) {
      return
    }

    const ctx = canvas.getContext("2d")
    if (!ctx) {
      return
    }

    ctx.clearRect(0, 0, canvas.width, canvas.height)
    ctx.fillStyle = "#111827"
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    if (!payload || !bounds || visibleQuads.length === 0) {
      ctx.fillStyle = "#d1d5db"
      ctx.font = "16px sans-serif"
      ctx.fillText("Load a prototype scene to preview quads.", 20, 28)
      return
    }

    const contentWidth = Math.max(bounds.maxX - bounds.minX, 1)
    const contentHeight = Math.max(bounds.maxY - bounds.minY, 1)
    const padding = 20
    const sx = (canvas.width - padding * 2) / contentWidth
    const sy = (canvas.height - padding * 2) / contentHeight
    const scale = Math.max(0.1, Math.min(sx, sy))

    for (const quad of visibleQuads) {
      ctx.beginPath()
      quad.screen.forEach(([x, y], index) => {
        const px = (x - bounds.minX) * scale + padding
        const py = (y - bounds.minY) * scale + padding
        if (index === 0) {
          ctx.moveTo(px, py)
        } else {
          ctx.lineTo(px, py)
        }
      })
      ctx.closePath()

      const color = COLORS[quad.layer] ?? "#a3a3a3"
      ctx.globalAlpha = Math.max(0.2, Math.min(1, quad.brightness))
      ctx.fillStyle = color
      ctx.fill()

      ctx.globalAlpha = 0.95
      ctx.strokeStyle = "#0b1020"
      ctx.lineWidth = 1
      ctx.stroke()
    }

    ctx.globalAlpha = 1
  }, [payload, bounds, visibleQuads])

  return <canvas ref={canvasRef} width={760} height={420} style={{ borderRadius: 8, border: "1px solid #374151" }} />
}
