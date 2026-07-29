import { useEffect, useState } from "react";

import { App as MCPApp } from "@modelcontextprotocol/ext-apps";

import {
    ReactFlow,
    Background,
    Controls,
    MiniMap,
} from "@xyflow/react";

import { layoutGraph } from "./layout";


export default function App() {
    
    const [nodes, setNodes] = useState([]);
    const [edges, setEdges] = useState([]);

    useEffect(() => {

        const app = new MCPApp({
            name: "data_model_view",
            version: "1.0.0"
        });

        app.ontoolresult = async (result) => {
            
            const structured = await layoutGraph(
                result.structuredContent.nodes,
                result.structuredContent.edges
            );
        
            setNodes(structured.nodes);
            setEdges(structured.edges);

        };

        app.connect();

    }, []);
    
    
    return (
        <div style={{ width: "100vw", height: "100vh" }}>
            <ReactFlow
                nodes={nodes}
                edges={edges}
                fitView
            >
                <Background/>
                <MiniMap/>
                <Controls/>
            </ReactFlow>
        </div>
    );

}