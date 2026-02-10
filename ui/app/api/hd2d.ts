import axios from "axios"

const BASE_URL = "http://127.0.0.1:5001"

export type Hd2dGame = "alttp" | "chrono_trigger"

export interface Hd2dQuad {
  layer: string
  kind: string
  world: [number, number, number][]
  screen: [number, number][]
  brightness: number
}

export interface Hd2dPayload {
  game_id: Hd2dGame
  camera: {
    yaw_deg: number
    pitch_deg: number
    zoom: number
  }
  quad_count: number
  quads: Hd2dQuad[]
}

export async function getHd2dPrototype(params: {
  game: Hd2dGame
  yaw?: number
  pitch?: number
  zoom?: number
}) {
  const response = await axios.get<Hd2dPayload>(`${BASE_URL}/hd2d/prototype`, {
    params,
  })
  return response.data
}
