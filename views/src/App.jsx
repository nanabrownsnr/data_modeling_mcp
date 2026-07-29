import { useEffect, useState } from "react";

import { App as MCPApp } from "@modelcontextprotocol/ext-apps";

import {
    ReactFlow,
    Background,
    Controls,
    MiniMap,
} from "@xyflow/react";


export default function App() {
    

    const [nodes, setNodes] = useState([]);
    const [edges, setEdges] = useState([]);


    useEffect(() => {

        const app = new MCPApp({
            name: "data_model_view",
            version: "1.0.0"
        });

        app.ontoolresult = (result) => {

            console.log("MCP RESULT:", result);

            setNodes(result.structuredContent?.nodes ?? []);
            setEdges(result.structuredContent?.edges ?? []);

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