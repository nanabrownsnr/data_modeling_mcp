import ELK from "elkjs/lib/elk.bundled.js";

const elk = new ELK();

export async function layoutGraph(nodes, edges) {

    const graph = {
        id: "root",

        layoutOptions: {
            "elk.algorithm": "layered",
            "elk.direction": "RIGHT"
        },

        children: nodes.map(node => ({
            id: node.id,
            width: 180,
            height: 80
        })),

        edges: edges.map(edge => ({
            id: edge.id,
            sources: [edge.source],
            targets: [edge.target]
        }))
    };

    const layout = await elk.layout(graph);

    const laidOutNodes = nodes.map(node => {

        const elkNode = layout.children.find(n => n.id === node.id);

        return {
            ...node,
            position: {
                x: elkNode.x,
                y: elkNode.y
            }
        };

    });

    return {
        nodes: laidOutNodes,
        edges
    };

}