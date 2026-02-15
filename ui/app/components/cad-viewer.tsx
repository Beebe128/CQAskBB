"use client"

import { useEffect, useMemo, useRef } from 'react'
import "../../dist/three-cad-viewer/three-cad-viewer.css"
import { Viewer } from "../../dist/three-cad-viewer/three-cad-viewer.esm.js"

function nc(change) {}

export interface CadViewerProps {
  cadShapes: any
}

export default function CadViewer({ cadShapes }: CadViewerProps) {
  const ref = useRef<HTMLDivElement | null>(null)

  const viewerOptions = useMemo(() => {
    const width = typeof window === 'undefined' ? 1280 : window.innerWidth
    const height = typeof window === 'undefined' ? 720 : window.innerHeight

    return {
      theme: "light",
      ortho: true,
      control: "trackball",
      normalLen: 0,
      cadWidth: width,
      height: height * 0.85,
      ticks: 10,
      ambientIntensity: 0.9,
      directIntensity: 0.12,
      transparent: false,
      blackEdges: false,
      axes: true,
      grid: [false, false, false],
      timeit: false,
      rotateSpeed: 1,
      tools: false,
      glass: false
    }
  }, [])

  const renderOptions = useMemo(() => ({
    ambientIntensity: 1.0,
    directIntensity: 1.1,
    metalness: 0.30,
    roughness: 0.65,
    edgeColor: 0x707070,
    defaultOpacity: 0.5,
    normalLen: 0,
    up: "Z"
  }), [])

  useEffect(() => {
    const container = ref.current
    if (!container) {
      return
    }

    if (cadShapes && cadShapes.length > 0) {
      const viewer = new Viewer(container, viewerOptions, nc)

      const render = (name: string, shapes, states) => {
        viewer?.clear()
        const [unselected, selected] = viewer.renderTessellatedShapes(shapes, states, renderOptions)

        viewer.render(
          unselected,
          selected,
          states,
          renderOptions,
        )
      }

      render("input", ...cadShapes)
    }
  }, [cadShapes, renderOptions, viewerOptions])

  return (
    <div ref={ref}></div>
  )
}
