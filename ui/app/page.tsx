"use client"

import { Alert, Button, Checkbox, InputNumber, Layout, Select, Space, theme, Typography } from 'antd'
import Search from 'antd/es/input/Search'
import { useMemo, useState } from 'react'
import { getCadDownload as downloadCadFile, getCadShapes as getCadObject } from './api/cad'
import { Hd2dGame, Hd2dPayload, getHd2dPrototype } from './api/hd2d'
import CadViewer from './components/cad-viewer'
import Hd2dViewer from './components/hd2d-viewer'
const { Content } = Layout
const { Title, Text } = Typography

export default function Home() {
  const {
    token: { colorBgContainer },
  } = theme.useToken()

  const [cadShapes, setCadShapes] = useState([])
  const [isError, setIsError] = useState(false)
  const [cadID, setCadID] = useState<string>()

  const [hd2dGame, setHd2dGame] = useState<Hd2dGame>('alttp')
  const [hd2dYaw, setHd2dYaw] = useState<number>(8)
  const [hd2dPitch, setHd2dPitch] = useState<number>(12)
  const [hd2dZoom, setHd2dZoom] = useState<number>(1.1)
  const [hd2dPayload, setHd2dPayload] = useState<Hd2dPayload>()
  const [hd2dError, setHd2dError] = useState<string>()
  const [hiddenLayers, setHiddenLayers] = useState<string[]>([])

  const layerNames = useMemo(() => {
    if (!hd2dPayload) {
      return []
    }
    return [...new Set(hd2dPayload.quads.map((quad) => quad.layer))]
  }, [hd2dPayload])

  const visibleQuadCount = useMemo(() => {
    if (!hd2dPayload) {
      return 0
    }
    const hiddenSet = new Set(hiddenLayers)
    return hd2dPayload.quads.filter((quad) => !hiddenSet.has(quad.layer)).length
  }, [hd2dPayload, hiddenLayers])

  const onSearch = async (value: string) => {
    try {
      setIsError(false)
      const cadObject = await getCadObject(value)
      setCadShapes(cadObject.shapes)
      setCadID(cadObject.id)
      setIsError(false)
    } catch {
      setIsError(true)
    }
  }

  const onDownload = async (file_type: 'stl' | 'step') => {
    if (cadID) {
      await downloadCadFile(cadID, file_type)
    }
  }

  const onRunHd2d = async () => {
    try {
      setHd2dError(undefined)
      const payload = await getHd2dPrototype({
        game: hd2dGame,
        yaw: hd2dYaw,
        pitch: hd2dPitch,
        zoom: hd2dZoom,
      })
      setHd2dPayload(payload)
      setHiddenLayers([])
    } catch {
      setHd2dError('Could not load HD-2D prototype payload. Is backend running on :5001?')
    }
  }

  return (
    <Layout style={{ height: '100vh' }}>
      <Space wrap>
        <Select
          placeholder='Download'
          value={'Download'}
          style={{ width: 120 }}
          onChange={onDownload}
          options={[
            { value: 'py', label: 'Cadquery PY' },
            { value: 'step', label: 'STEP' },
            { value: 'stl', label: 'STL' },
            { value: 'amf', label: 'AMF' },
            { value: '3mf', label: '3MF' },
            { value: 'vrml', label: 'VRML' },
          ]}
        />
      </Space>

      <Layout>
        <Layout style={{ padding: '0 24px 24px' }}>
          <Content
            style={{
              margin: 0,
              minHeight: 280,
              background: colorBgContainer,
            }}
          >
            <Layout>
              <CadViewer cadShapes={cadShapes} />
            </Layout>
          </Content>

          {isError ? (
            <Space direction='vertical' style={{ width: '100%' }}>
              <Alert
                message='Error Generating'
                description="Please try again. To debug check logs and 'generated' directory for latest file"
                type='error'
              />
            </Space>
          ) : null}

          <Search placeholder='input search text' size='large' onSearch={onSearch} />

          <div style={{ marginTop: 24 }}>
            <Title level={4}>HD-2D Prototype Viewer</Title>
            <Space wrap>
              <Select
                value={hd2dGame}
                onChange={setHd2dGame}
                options={[
                  { value: 'alttp', label: 'A Link to the Past' },
                  { value: 'chrono_trigger', label: 'Chrono Trigger' },
                ]}
                style={{ width: 220 }}
              />
              <InputNumber value={hd2dYaw} onChange={(v) => setHd2dYaw(v ?? 0)} addonBefore='Yaw' />
              <InputNumber value={hd2dPitch} onChange={(v) => setHd2dPitch(v ?? 0)} addonBefore='Pitch' />
              <InputNumber value={hd2dZoom} onChange={(v) => setHd2dZoom(v ?? 1)} addonBefore='Zoom' step={0.05} />
              <Button type='primary' onClick={onRunHd2d}>
                Load Prototype
              </Button>
            </Space>
            <div style={{ marginTop: 10 }}>
              <Text type='secondary'>Renders projected quads from backend /hd2d/prototype.</Text>
            </div>

            {layerNames.length > 0 ? (
              <div style={{ marginTop: 12 }}>
                <Text strong>Visible layers</Text>
                <div style={{ marginTop: 8 }}>
                  <Checkbox.Group
                    value={layerNames.filter((layer) => !hiddenLayers.includes(layer))}
                    options={layerNames.map((layer) => ({ label: layer, value: layer }))}
                    onChange={(selected) => {
                      const selectedSet = new Set(selected as string[])
                      const nextHidden = layerNames.filter((layer) => !selectedSet.has(layer))
                      setHiddenLayers(nextHidden)
                    }}
                  />
                </div>
              </div>
            ) : null}

            {hd2dError ? <Alert style={{ marginTop: 12 }} message={hd2dError} type='error' /> : null}
            <div style={{ marginTop: 12 }}>
              <Hd2dViewer payload={hd2dPayload} hiddenLayers={hiddenLayers} />
            </div>
            {hd2dPayload ? (
              <div style={{ marginTop: 8 }}>
                <Text>
                  Game: {hd2dPayload.game_id} · Quads: {visibleQuadCount}/{hd2dPayload.quad_count} visible · Camera:
                  y={hd2dPayload.camera.yaw_deg}, p={hd2dPayload.camera.pitch_deg}, z={hd2dPayload.camera.zoom}
                </Text>
              </div>
            ) : null}
          </div>
        </Layout>
      </Layout>
    </Layout>
  )
}
