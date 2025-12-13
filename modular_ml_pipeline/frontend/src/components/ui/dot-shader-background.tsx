import { useMemo, useEffect, useState } from 'react'
import { Canvas, ThreeEvent, useFrame, useThree, extend } from '@react-three/fiber'
import { shaderMaterial } from '@react-three/drei'
import * as THREE from 'three'

const DotMaterial = shaderMaterial(
  {
    time: 0,
    resolution: new THREE.Vector2(),
    dotColor: new THREE.Color('#FFFFFF'),
    bgColor: new THREE.Color('#121212'),
    mouseTrail: null,
    render: 0,
    rotation: 0,
    gridSize: 50,
    dotOpacity: 0.05
  },
  /* glsl */ `
    void main() {
      gl_Position = vec4(position.xy, 0.0, 1.0);
    }
  `,
  /* glsl */ `
    uniform float time;
    uniform int render;
    uniform vec2 resolution;
    uniform vec3 dotColor;
    uniform vec3 bgColor;
    uniform sampler2D mouseTrail;
    uniform float rotation;
    uniform float gridSize;
    uniform float dotOpacity;

    vec2 rotate(vec2 uv, float angle) {
        float s = sin(angle);
        float c = cos(angle);
        mat2 rotationMatrix = mat2(c, -s, s, c);
        return rotationMatrix * (uv - 0.5) + 0.5;
    }

    vec2 coverUv(vec2 uv) {
      vec2 s = resolution.xy / max(resolution.x, resolution.y);
      vec2 newUv = (uv - 0.5) * s + 0.5;
      return clamp(newUv, 0.0, 1.0);
    }

    float sdfCircle(vec2 p, float r) {
        return length(p - 0.5) - r;
    }

    void main() {
      vec2 screenUv = gl_FragCoord.xy / resolution;
      vec2 uv = coverUv(screenUv);

      vec2 rotatedUv = rotate(uv, rotation);

      // Create a grid
      vec2 gridUv = fract(rotatedUv * gridSize);
      vec2 gridUvCenterInScreenCoords = rotate((floor(rotatedUv * gridSize) + 0.5) / gridSize, -rotation);

      // Calculate distance from the center of each cell
      float baseDot = sdfCircle(gridUv, 0.25);

      // Screen mask
      float screenMask = smoothstep(0.0, 1.0, 1.0 - uv.y); // 0 at the top, 1 at the bottom
      vec2 centerDisplace = vec2(0.7, 1.1);
      float circleMaskCenter = length(uv - centerDisplace);
      float circleMaskFromCenter = smoothstep(0.5, 1.0, circleMaskCenter);
      
      float combinedMask = screenMask * circleMaskFromCenter;
      float circleAnimatedMask = sin(time * 2.0 + circleMaskCenter * 10.0);

      // Mouse trail effect
      float mouseInfluence = texture2D(mouseTrail, gridUvCenterInScreenCoords).r;
      
      float scaleInfluence = max(mouseInfluence * 0.5, circleAnimatedMask * 0.3);

      // Create dots with animated scale, influenced by mouse
      float dotSize = min(pow(circleMaskCenter, 2.0) * 0.3, 0.3);

      float sdfDot = sdfCircle(gridUv, dotSize * (1.0 + scaleInfluence * 0.5));

      float smoothDot = smoothstep(0.05, 0.0, sdfDot);

      float opacityInfluence = max(mouseInfluence * 50.0, circleAnimatedMask * 0.5);

      // Mix background color with dot color, using animated opacity to increase visibility
      vec3 composition = mix(bgColor, dotColor, smoothDot * combinedMask * dotOpacity * (1.0 + opacityInfluence));

      gl_FragColor = vec4(composition, 1.0);
    }
  `
)

extend({ DotMaterial })

declare global {
  namespace JSX {
    interface IntrinsicElements {
      dotMaterial: any
    }
  }
}

function Scene() {
  const size = useThree((s) => s.size)
  const viewport = useThree((s) => s.viewport)
  
  const rotation = 0
  const gridSize = 100

  // Use dark theme colors (since we're not using next-themes)
  const themeColors = {
    dotColor: '#FFFFFF',
    bgColor: '#121212',
    dotOpacity: 0.025
  }

  // Create a simple trail texture manually since useTrailTexture might not be available
  const [trailTexture, setTrailTexture] = useState<THREE.DataTexture | null>(null)
  const [mousePos, setMousePos] = useState<{ x: number; y: number }>({ x: 0.5, y: 0.5 })

  useEffect(() => {
    // Create a simple data texture for mouse trail
    const size = 512
    const data = new Uint8Array(size * size * 4)
    const texture = new THREE.DataTexture(data, size, size, THREE.RGBAFormat)
    texture.needsUpdate = true
    setTrailTexture(texture)
  }, [])

  // Update trail texture continuously
  useFrame(() => {
    if (!trailTexture) return
    
    const size = 512
    const data = trailTexture.image.data
    const fadeRate = 0.95
    
    // Fade existing trail
    for (let i = 0; i < data.length; i += 4) {
      data[i] = Math.max(0, data[i] * fadeRate) // R
      data[i + 1] = Math.max(0, data[i + 1] * fadeRate) // G
      data[i + 2] = Math.max(0, data[i + 2] * fadeRate) // B
      data[i + 3] = Math.max(0, data[i + 3] * fadeRate) // A
    }
    
    // Add new mouse position
    const x = Math.floor(mousePos.x * size)
    const y = Math.floor(mousePos.y * size)
    const radius = 20
    
    for (let dy = -radius; dy <= radius; dy++) {
      for (let dx = -radius; dx <= radius; dx++) {
        const dist = Math.sqrt(dx * dx + dy * dy)
        if (dist <= radius) {
          const px = (x + dx + size) % size
          const py = (y + dy + size) % size
          const idx = (py * size + px) * 4
          const intensity = (1 - dist / radius) * 255
          data[idx] = Math.min(255, data[idx] + intensity)
          data[idx + 1] = Math.min(255, data[idx + 1] + intensity)
          data[idx + 2] = Math.min(255, data[idx + 2] + intensity)
          data[idx + 3] = Math.min(255, data[idx + 3] + intensity)
        }
      }
    }
    
    trailTexture.needsUpdate = true
  })

  const dotMaterial = useMemo(() => {
    const material = new DotMaterial()
    return material
  }, [])

  useEffect(() => {
    if (dotMaterial && dotMaterial.uniforms) {
      dotMaterial.uniforms.dotColor.value.setHex(parseInt(themeColors.dotColor.replace('#', '0x'), 16))
      dotMaterial.uniforms.bgColor.value.setHex(parseInt(themeColors.bgColor.replace('#', '0x'), 16))
      dotMaterial.uniforms.dotOpacity.value = themeColors.dotOpacity
    }
  }, [dotMaterial])

  useFrame((state) => {
    if (dotMaterial && dotMaterial.uniforms) {
      dotMaterial.uniforms.time.value = state.clock.elapsedTime
      dotMaterial.uniforms.resolution.value.set(size.width * viewport.dpr, size.height * viewport.dpr)
      dotMaterial.uniforms.rotation.value = rotation
      dotMaterial.uniforms.gridSize.value = gridSize
      if (trailTexture) {
        dotMaterial.uniforms.mouseTrail.value = trailTexture
      }
    }
  })

  const handlePointerMove = (e: ThreeEvent<PointerEvent>) => {
    // Convert pointer position to normalized coordinates
    const x = (e.uv?.x ?? 0.5)
    const y = (e.uv?.y ?? 0.5)
    setMousePos({ x, y })
  }

  const scale = Math.max(viewport.width, viewport.height) / 2

  return (
    <mesh scale={[scale, scale, 1]} onPointerMove={handlePointerMove}>
      <planeGeometry args={[2, 2]} />
      <dotMaterial />
    </mesh>
  )
}

export const DotScreenShader = () => {
  return (
    <Canvas
      gl={{
        antialias: true,
        powerPreference: 'high-performance',
        outputColorSpace: THREE.SRGBColorSpace,
        toneMapping: THREE.NoToneMapping
      }}
      style={{ width: '100%', height: '100%' }}
    >
      <Scene />
    </Canvas>
  )
}

export default DotScreenShader

